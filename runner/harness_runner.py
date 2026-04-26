#!/usr/bin/env python3
"""Minimal Harness v4 runner.

This runner intentionally implements only the JSON Schema subset used by this
repository. It validates an object, writes a snapshot artifact, and reads it
back to prove the artifact is addressable.
"""

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
DEFAULT_ARTIFACT_ROOT = ROOT / "artifacts" / "runner"


class ValidationError(Exception):
    pass


def load_json(path):
    with Path(path).open("r", encoding="utf-8") as fh:
        return json.load(fh)


def schema_path(schema_name):
    name = schema_name
    if not name.endswith(".schema.json"):
        name = f"{name}.schema.json"
    path = SCHEMA_DIR / name
    if not path.exists():
        raise SystemExit(f"schema not found: {path}")
    return path


def load_schema(schema_name):
    return load_json(schema_path(schema_name))


def load_common_defs():
    common = load_json(SCHEMA_DIR / "common.schema.json")
    return common.get("$defs", {})


def type_matches(value, expected):
    mapping = {
        "object": dict,
        "array": list,
        "string": str,
        "integer": int,
        "boolean": bool,
        "null": type(None),
    }
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    return isinstance(value, mapping[expected])


def resolve_ref(ref, common_defs):
    prefix = "common.schema.json#/$defs/"
    local_prefix = "#/$defs/"
    if ref.startswith(prefix):
        name = ref[len(prefix):]
        if name not in common_defs:
            raise ValidationError(f"missing common $defs reference: {name}")
        return common_defs[name]
    if ref.startswith(local_prefix):
        name = ref[len(local_prefix):]
        if name not in common_defs:
            raise ValidationError(f"missing local $defs reference: {name}")
        return common_defs[name]
    raise ValidationError(f"unsupported $ref: {ref}")


def validate(value, schema, common_defs, path="$"):
    if "$ref" in schema:
        return validate(value, resolve_ref(schema["$ref"], common_defs), common_defs, path)

    if "oneOf" in schema:
        errors = []
        for option in schema["oneOf"]:
            try:
                validate(value, option, common_defs, path)
                return
            except ValidationError as exc:
                errors.append(str(exc))
        raise ValidationError(f"{path}: did not match any oneOf option: {errors}")

    if "const" in schema and value != schema["const"]:
        raise ValidationError(f"{path}: expected const {schema['const']!r}, got {value!r}")

    if "enum" in schema and value not in schema["enum"]:
        raise ValidationError(f"{path}: expected one of {schema['enum']!r}, got {value!r}")

    expected_type = schema.get("type")
    if isinstance(expected_type, list):
        if not any(type_matches(value, t) for t in expected_type):
            raise ValidationError(f"{path}: expected type {expected_type!r}, got {type(value).__name__}")
    elif isinstance(expected_type, str):
        if not type_matches(value, expected_type):
            raise ValidationError(f"{path}: expected type {expected_type!r}, got {type(value).__name__}")

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            raise ValidationError(f"{path}: string shorter than minLength {schema['minLength']}")
        if "pattern" in schema and not re.match(schema["pattern"], value):
            raise ValidationError(f"{path}: string does not match pattern {schema['pattern']!r}")

    if isinstance(value, int) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            raise ValidationError(f"{path}: integer below minimum {schema['minimum']}")

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            raise ValidationError(f"{path}: array shorter than minItems {schema['minItems']}")
        if "items" in schema:
            for idx, item in enumerate(value):
                validate(item, schema["items"], common_defs, f"{path}[{idx}]")
        if "contains" in schema:
            for item in value:
                try:
                    validate(item, schema["contains"], common_defs, path)
                    break
                except ValidationError:
                    continue
            else:
                raise ValidationError(f"{path}: array does not contain required element")

    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                raise ValidationError(f"{path}: missing required field {key!r}")

        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extra = sorted(set(value) - set(properties))
            if extra:
                raise ValidationError(f"{path}: unexpected fields {extra!r}")

        for key, child_schema in properties.items():
            if key in value:
                validate(value[key], child_schema, common_defs, f"{path}.{key}")


def validate_file(schema_name, input_path):
    schema = load_schema(schema_name)
    common_defs = load_common_defs()
    data = load_json(input_path)
    validate(data, schema, common_defs)
    return schema, data


def artifact_name(schema_name, data):
    uid = data.get("run_uid") or data.get("issue_uid") or data.get("rule_uid") or data.get("tool_uid") or data.get("memory_uid") or "object"
    safe_uid = re.sub(r"[^A-Za-z0-9._:-]+", "_", str(uid))
    safe_schema = schema_name.replace(".schema.json", "")
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return f"{stamp}_{safe_schema}_{safe_uid}.json"


def write_artifact(schema_name, data, artifact_root):
    root = Path(artifact_root)
    root.mkdir(parents=True, exist_ok=True)
    path = root / artifact_name(schema_name, data)
    payload = {
        "schema": schema_name if schema_name.endswith(".schema.json") else f"{schema_name}.schema.json",
        "written_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "data": data,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def readback(path):
    payload = load_json(path)
    if "schema" not in payload or "data" not in payload or "written_at" not in payload:
        raise ValidationError(f"artifact readback failed: {path}")
    return payload


def list_schemas():
    for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        if path.name != "common.schema.json":
            print(path.name)


def cmd_validate(args):
    validate_file(args.schema, args.input)
    print(json.dumps({"result": "pass", "schema": args.schema, "input": args.input}, ensure_ascii=False))


def cmd_run(args):
    schema, data = validate_file(args.schema, args.input)
    out = write_artifact(Path(schema_path(args.schema)).name, data, args.artifact_root)
    readback(out)
    print(json.dumps({
        "result": "pass",
        "schema": schema.get("title"),
        "artifact_path": str(out),
        "readback_status": "pass",
    }, ensure_ascii=False, indent=2))


def build_parser():
    parser = argparse.ArgumentParser(description="Minimal Harness v4 schema runner")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list-schemas", help="List available object schemas")

    validate_parser = sub.add_parser("validate", help="Validate a JSON object against a schema")
    validate_parser.add_argument("--schema", required=True, help="Schema file name or object name")
    validate_parser.add_argument("--input", required=True, help="JSON input file")

    run_parser = sub.add_parser("run", help="Validate, write artifact, and read it back")
    run_parser.add_argument("--schema", required=True, help="Schema file name or object name")
    run_parser.add_argument("--input", required=True, help="JSON input file")
    run_parser.add_argument("--artifact-root", default=str(DEFAULT_ARTIFACT_ROOT), help="Artifact output directory")

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "list-schemas":
            list_schemas()
        elif args.command == "validate":
            cmd_validate(args)
        elif args.command == "run":
            cmd_run(args)
        else:
            parser.error(f"unknown command: {args.command}")
    except (ValidationError, json.JSONDecodeError, OSError) as exc:
        print(json.dumps({"result": "fail", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
