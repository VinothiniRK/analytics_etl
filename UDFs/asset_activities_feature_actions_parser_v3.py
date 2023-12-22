def asset_activities_feature_actions_parser_v3(all_changes, action_details_by_name, actor, payload_type):
    if actor['type'] == 19:
        return workflow_action_parser(all_changes, action_details_by_name, actor)
    else:
        return feature_actions_parser(all_changes, action_details_by_name, actor, payload_type)
        
def workflow_action_parser(all_changes, action_details_by_name, actor):
    formated_custom_fields = []
    if 'is_discovery_enabled' in all_changes['model_changes']:
        for system_change in  all_changes['system_changes']:
            if 'disable_asset_discovery' in system_change["changes"]:
                action_details = get_performed_by_parser(actor, system_change['name'])
                action_details.update(action_details_by_name['config_item_discovery_disabled'])
                action_details['field_type'] = "asset_actions"
                formated_custom_fields.append(action_details)
    return formated_custom_fields
    
def feature_actions_parser(all_changes, action_details_by_name, actor, payload_type):
    formated_custom_fields = []
    performed_by = get_performed_by_parser(actor, None)
    if (payload_type in action_details_by_name):
        action_details = performed_by.copy()
        action_details.update(action_details_by_name[payload_type])
        action_details['field_type'] = "asset_actions"
        formated_custom_fields.append(action_details)
    
    for change_name, change in all_changes["model_changes"].items():
        action_details, action_name = performed_by.copy(), ""
        if change_name in ['tickets', 'changes', 'problems', 'releases']:
            module = change_name[:-1]
            action = list(change.keys())[0]
            action_name = '%s_%s'%(module, action)
            action_details['to_value'] = '%s(#%s)'%(change[action]['subject'], change[action]['human_display_id'])
            action_details['to_value_string'] = action_details['to_value']
        elif change_name == 'freshrelease_properties':
            item_type = change['fr_item_type']
            action = change['action']
            action_name = '%s_%s'%(item_type, action)
            action_details['to_value'] = change['name']
            action_details['to_value_string'] = change['name']
        elif change_name == 'deleted':
            action_name = 'config_item_trashed' if change[1] else 'config_item_restore'
            action_details['to_value'] = change[1]
            action_details['column_name'] = "to_boolean_value"
        elif change_name == 'disabled':
            action_name = 'config_item_disabled'  if change[1] else 'config_item_enabled'
        elif change_name == 'is_discovery_enabled':
            action_name = 'config_item_discovery_enabled'  if change[1] else 'config_item_discovery_disabled'
        
        if action_name in action_details_by_name:
            action_details.update(action_details_by_name[action_name])
            action_details['field_type'] = "asset_actions"
            if action_details.get('column_name') is not None:
                action_details['to_column_name'] = action_details.pop('column_name', None)
            formated_custom_fields.append(action_details)
            action_name = ""
    return formated_custom_fields    
    
def dig(dictionary, *keys):
    for key in keys:
        if isinstance(dictionary, (dict)) and key in dictionary:
            dictionary = dictionary[key]
        elif isinstance(dictionary, (str, list, tuple, set)) and key < len(dictionary) and key >= -len(dictionary):
            dictionary = dictionary[key]
        else:
            return None
    return dictionary
    
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