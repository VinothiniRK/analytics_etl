def asset_activities_application_installation_parser_v2(payload, action_details_by_name, payload_type):
    formated_custom_fields = []
    if(payload_type in ["cmdb_application_installation_create", "cmdb_application_installation_update", "cmdb_application_installation_destroy"]):
        action_details = get_performed_by_parser(payload['actor'], dig(payload, 'changes', 'system_changes', 0, 'name'))
        action_details.update(action_details_by_name[payload_type])
        action_details["to_value"] = payload["associations"]["application"]["name"]
        app_version = dig(payload, "model_properties", "application_version")
        if app_version is not None: 
            action_details["to_value"] += " (%s)"%(app_version)
        update_common_details(payload["associations"]["config_item"], action_details)
        formated_custom_fields.append(action_details)
    return formated_custom_fields

def update_common_details(config_item, action_details):
    action_details['asset_id'] = config_item["id"]
    if "column_name" in action_details:
        action_details['to_column_name'] = action_details.pop('column_name')
    if "workspace_id" in config_item:
        action_details['workspace_id'] = config_item["workspace_id"]
    if action_details["to_value"] is not None:
        action_details['to_value_string'] = str(action_details["to_value"])

def get_performed_by_parser(actor, workflow_name):
    performed_by = {}
    if actor['type'] == 19: # Asset Workflow
        performed_by['system_user_type'] = actor['name']
        performed_by['system_user_name'] = workflow_name
    elif actor['type'] == 100: # Discovery sources
        performed_by['system_user_type'] = actor['name']
    elif actor['type'] == 0: # User
        performed_by['actor_id'] = actor['id']
        performed_by['system_user_name'] = actor['name']
        performed_by['system_user_type'] = "User"
    return performed_by

def dig(dictionary, *keys):
    for key in keys:
        if isinstance(dictionary, (dict)) and key in dictionary:
            dictionary = dictionary[key]
        elif isinstance(dictionary, (str, list, tuple, set)) and key < len(dictionary) and key >= -len(dictionary):
            dictionary = dictionary[key]
        else:
            return None
    return dictionary