PAYLOAD_SCHEMA = {
    "type": "object",
    "required": ["extents", "source"],
    "properties": {
        "description": {
            "type": "string"
        },
        "extents": {
            "$ref": "#/definitions/feature_collection"
        },
        "source": {
            "type": "string"
        }
    },

    "definitions": {

        "feature_collection": {
            "type": "object",
            "required": ["type", "features"],
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["FeatureCollection"]
                },
                "features": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/feature"
                    }
                }
            }
        },

        "feature": {
            "type": "object",
            "required": ["type", "geometry", "properties"],
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["Feature"]
                },
                "geometry": {
                    "type": "object",
                    "oneOf": [
                        {
                            "$ref": "#/definitions/polygon"
                        },
                        {
                            "$ref": "#/definitions/multi_polygon"
                        }
                    ]
                },
                "properties": {
                    "oneOf": [
                        {
                            "type": "object"
                        },
                        {
                            "type": "null"
                        }
                    ]
                },
            }
        },

        "point": {
            "type": "array",
            "minItems": 2,
            "maxItems": 2,
            "items": {
                "type": "number"
            }
        },

        "polygon": {
            "type": "object",
            "required": ["coordinates", "type"],
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["Polygon"]
                },
                "coordinates": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {
                            "$ref": "#/definitions/point"
                        }
                    }
                }
            }
        },

        "multi_polygon": {
            "type": "object",
            "required": ["coordinates", "type"],
            "properties": {
                "type": {
                    "type": "string",
                    "enum": ["MultiPolygon"]
                },
                "coordinates": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/point"
                            }
                        }
                    }
                }
            }
        }
    }
}
