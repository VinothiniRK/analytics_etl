def asset_activities_relationship_parser_v2(payload, action_details_by_name):
    formated_custom_fields = []
    model_properties = payload["model_properties"]
    if model_properties["primary_type"] == "Cmdb::ConfigItem":
        stream_flow = "downstream_relation"
        action_details = get_performed_by_parser(payload['actor'], dig(payload, 'changes', 'system_changes', 0, 'name'))
        action_details.update(action_details_by_name["%s_%s"%(stream_flow,payload["action"])])
        update_relationship_details(model_properties['secondary_type'], payload["associations"], stream_flow, action_details)
        formated_custom_fields.append(action_details)
    if model_properties["secondary_type"] == "Cmdb::ConfigItem":
        stream_flow = "upstream_relation"
        action_details = get_performed_by_parser(payload['actor'], dig(payload, 'changes', 'system_changes', 0, 'name'))
        action_details.update(action_details_by_name["%s_%s"%(stream_flow,payload["action"])])
        update_relationship_details(model_properties['primary_type'], payload["associations"], stream_flow, action_details)
        formated_custom_fields.append(action_details)
    return formated_custom_fields

def update_relationship_details(model_type, associations, stream_flow, action_details):
    parent_type, child_type = ["primary", "secondary"] if(stream_flow == "downstream_relation") else ["secondary", "primary"]
    child_entity = associations[child_type]
    model_mapping = {
        "Cmdb::ConfigItem": "Asset-%s"%(dig(child_entity, "display_id")),
        "User": "Requester",
        "Agent": "Agent",
        "Itil::Department": "Department",
        "Cmdb::Application": "Software"
    }
    stream = associations["relationship"][stream_flow]
    name = child_entity["name"]
    typ = model_mapping[model_type]
    action_details["to_value"] = "%s with %s(%s)"%(stream, name, typ)
    update_common_details(associations[parent_type], action_details)
    
def update_common_details(config_item, action_details):
    action_details['asset_id'] = config_item["id"]
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