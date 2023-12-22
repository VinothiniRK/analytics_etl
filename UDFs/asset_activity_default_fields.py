def asset_activity_default_fields(only_values):
    hsh = {
        "name":{
            "action_id": 1, "field_type": "default_asset_fields", "col_type": "text", "action": "Name"
        },
        "asset_tag":{
            "action_id": 2, "field_type": "default_asset_fields", "col_type": "text", "action": "Asset Tag"
        },
        "ci_type_name":{
            "action_id": 3, "field_type": "default_asset_fields", "col_type": "dropdown", "action": "Asset Type"
        },
        "impact_name":{
            "action_id": 4, "field_type": "default_asset_fields", "col_type": "dropdown", "action": "Impact"
        },
        "description":{
            "action_id": 5, "field_type": "default_asset_fields", "col_type": "paragraph", "action": "Description"
        },
        "end_of_life":{
            "action_id": 6, "field_type": "default_asset_fields", "col_type": "date_only", "action": "End Of Life"
        },
        "location_name":{
            "action_id": 7, "field_type": "default_asset_fields", "col_type": "dropdown", "action": "Location"
        },
        "department_name":{
            "action_id": 8, "field_type": "default_asset_fields", "col_type": "dropdown", "action": "Department"
        },
        "agent_name":{
            "action_id": 9, "field_type": "default_asset_fields", "col_type": "dropdown", "action": "Managed By"
        },
        "workspace_name": {
            "action_id": 10, "field_type": "default_asset_fields", "col_type": "dropdown", "action": "Workspace"
        },
        "user_name":{
            "action_id": 11, "field_type": "default_asset_fields", "col_type": "dropdown", "action": "Used By"
        },
        "assigned_on":{
            "action_id": 12, "field_type": "default_asset_fields", "col_type": "date", "action": "Assigned On"
        },
        "group_name":{
            "action_id": 13, "field_type": "default_asset_fields", "col_type": "dropdown", "action": "Managed By Group"
        },
        "salvage":{
            "action_id": 14, "field_type": "default_asset_fields", "col_type": "number", "action": "Salvage"
        },
        "usage_type_name":{
            "action_id": 15, "field_type": "default_asset_fields", "col_type": "dropdown", "action": "Usage Type"
        },
        "depreciation_name":{
            "action_id": 16, "field_type": "default_asset_fields", "col_type": "dropdown", "action": "Depreciation"
        }
    }
    if only_values:
        return list(hsh.values())
    return hsh