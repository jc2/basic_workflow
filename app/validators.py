WORKFLOW_SCHEMA = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "steps": {
      "type": "array",
      "items": [
        {
          "type": "object",
          "properties": {
            "id": {
              "type": "string"
            },
            "params": {
              "type": "object",
              "patternProperties": {
                "^.*$": {
                  "type": "object",
                  "properties": {
                    "from_id": {
                      "type": [
                        "string",
                        "null"
                      ]
                    },
                    "param_id": {
                      "type": [
                        "string",
                        "null"
                      ]
                    },
                    "value": {
                      "type": [
                        "number",
                        "boolean"
                      ]
                    }
                  },
                  "required": [
                    "from_id"
                  ],
                  "oneOf": [
                    {
                      "required": [
                        "param_id"
                      ]
                    },
                    {
                      "required": [
                        "value"
                      ]
                    }
                  ]
                }
              },
              "additionalProperties": False
            },
            "action": {
              "type": "string"
            },
            "transitions": {
              "type": "array",
              "items": [
                {
                  "type": "object",
                  "properties": {
                    "condition": {
                      "type": "array",
                      "items": [
                        {
                          "type": "object",
                          "properties": {
                            "from_id": {
                              "type": "string"
                            },
                            "field_id": {
                              "type": "string"
                            },
                            "operator": {
                              "type": "string"
                            },
                            "value": {
                              "type": [
                                "number",
                                "boolean"
                              ]
                            }
                          },
                          "required": [
                            "from_id",
                            "field_id",
                            "operator",
                            "value"
                          ]
                        }
                      ]
                    },
                    "target": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "condition",
                    "target"
                  ]
                }
              ]
            }
          },
          "required": [
            "id",
            "params",
            "action",
            "transitions"
          ]
        }
      ]
    },
    "trigger": {
      "type": "object",
      "properties": {
        "params": {
          "type": "object",
          "patternProperties": {
            "^.*$": {
              "type": [
                "string",
                "number",
                "boolean"
              ]
            }
          },
          "additionalProperties": False
        },
        "transitions": {
          "type": "array",
          "items": [
            {
              "type": "object",
              "properties": {
                "target": {
                  "type": "string"
                },
                "condition": {
                  "type": "array",
                  "items": [
                    {
                      "type": "object",
                      "properties": {
                        "from_id": {
                          "type": "string"
                        },
                        "field_id": {
                          "type": "string"
                        },
                        "operator": {
                          "type": "string"
                        },
                        "value": {
                          "type": [
                            "number",
                            "boolean"
                          ]
                        }
                      },
                      "required": [
                        "from_id",
                        "field_id",
                        "operator",
                        "value"
                      ]
                    }
                  ]
                }
              },
              "required": [
                "target",
                "condition"
              ]
            }
          ]
        },
        "id": {
          "type": "string"
        }
      },
      "required": [
        "params",
        "transitions",
        "id"
      ]
    }
  },
  "required": [
    "steps",
    "trigger"
  ]
}
