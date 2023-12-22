def asset_activity_action_info(only_values, old_relationship):
    hsh = {
        'config_item_create': {'action_id': 1001, 'action':'Asset Created', 'field_type': 'asset_actions'},
        'config_item_trashed': {'action_id': 1002, 'action':'Asset Trashed', 'field_type': 'asset_actions'},
        'config_item_restore': {'action_id': 1003, 'action':'Asset Restored', 'field_type': 'asset_actions'},
        'config_item_enabled': {'action_id': 1004, 'action':'Asset Enabled', 'field_type': 'asset_actions'},
        'config_item_disabled': {'action_id': 1005, 'action':'Asset Disabled', 'field_type': 'asset_actions'},
        'config_item_discovery_enabled': {'action_id': 1006, 'action':'Asset Discovery Enabled', 'field_type': 'asset_actions'},
        'config_item_discovery_disabled': {'action_id': 1007, 'action':'Asset Discovery Disabled', 'field_type': 'asset_actions'},
        'ticket_added': {'action_id': 1008, 'action':'Ticket Associated','column_name': 'to_string_value', 'label':'Ticket Subject', 'field_type': 'asset_actions'},
        'ticket_removed': {'action_id': 1009, 'action':'Ticket Dissociated','column_name': 'to_string_value', 'label':'Ticket Subject', 'field_type': 'asset_actions'},
        'change_added': {'action_id': 1010, 'action':'Change Associated', 'column_name': 'to_string_value', 'label':'Change Subject', 'field_type': 'asset_actions'},
        'change_removed': {'action_id': 1011, 'action':'Change Dissociated', 'column_name': 'to_string_value', 'label':'Change Subject', 'field_type': 'asset_actions'},
        'problem_added': {'action_id': 1012, 'action':'Problem Associated', 'column_name': 'to_string_value', 'label':'Problem Subject', 'field_type': 'asset_actions'},
        'problem_removed': {'action_id': 1013, 'action':'Problem Dissociated', 'column_name': 'to_string_value', 'label':'Problem Subject', 'field_type': 'asset_actions'},
        'release_added': {'action_id': 1014, 'action':'Release Associated', 'column_name': 'to_string_value', 'label':'Release Subject', 'field_type': 'asset_actions'},
        'release_removed': {'action_id': 1015, 'action':'Release Dissociated', 'column_name': 'to_string_value', 'label':'Release Subject', 'field_type': 'asset_actions'},
        'project_attached': {'action_id': 1016, 'action':'Project Associated', 'column_name': 'to_string_value', 'label':'Project Subject', 'field_type': 'asset_actions'},
        'project_detached': {'action_id': 1017, 'action':'Project Dissociated', 'column_name': 'to_string_value', 'label':'Project Subject', 'field_type': 'asset_actions'},
        'issue_attached': {'action_id': 1018, 'action':'Project Task Associated', 'column_name': 'to_string_value', 'label':'Project Task Subject', 'field_type': 'asset_actions'},
        'issue_detached': {'action_id': 1019, 'action':'Project Task Dissociated', 'column_name': 'to_string_value', 'label':'Project Task Subject', 'field_type': 'asset_actions'},
        'upstream_relation_create': {'action_id': 1022,'action':'Upstream Relationship Added', 'column_name': 'to_string_value', 'label': 'Relationship Details', 'field_type': 'asset_actions'},
        'upstream_relation_destroy':{'action_id': 1023,'action':'Upstream Relationship Removed', 'column_name': 'to_string_value', 'label':'Relationship Details', 'field_type': 'asset_actions'},
        'downstream_relation_create':{'action_id': 1024,'action':'Downstream Relationship Added', 'column_name': 'to_string_value', 'label':'Relationship Details', 'field_type': 'asset_actions'},
        'downstream_relation_destroy':{'action_id': 1025,'action':'Downstream Relationship Removed', 'column_name': 'to_string_value', 'label':'Relationship Details', 'field_type': 'asset_actions'},
        'cmdb_application_installation_create':{'action_id': 1026,'action':'Software Added', 'column_name': 'to_string_value', 'label':'Software Name', 'field_type': 'asset_actions'},
        'cmdb_application_installation_update':{'action_id': 1027,'action':'Software Updated', 'column_name': 'to_string_value', 'label':'Software Name', 'field_type': 'asset_actions'},
        'cmdb_application_installation_destroy':{'action_id': 1028,'action':'Software Removed', 'column_name': 'to_string_value', 'label':'Software Name', 'field_type': 'asset_actions'}
    }
    old_relationship_hash =  {
        'relationship_added': {'action_id': 1020, 'action':'Relationship Added', 'column_name': 'to_string_value', 'label':'Relationship Details', 'field_type': 'asset_actions'},
        'relationship_removed':{'action_id': 1021,'action':'Relationship Removed', 'column_name': 'to_string_value', 'label':'Relationship Details', 'field_type': 'asset_actions'}
    }
    if old_relationship:
        # Combine the dictionaries
        combined_dict = {**hsh, **old_relationship_hash}
    else:
        # Return the first dictionary
        combined_dict = hsh
    if only_values:
        return list(combined_dict.values())
    return combined_dict