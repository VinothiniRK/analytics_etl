import html
import arrow
from dateutil import parser

def asset_activities_all_field_parser_v2(all_changes, field_details_by_name, column_lookup, actor):
    if actor['type'] == 19: # Asset Workflow
        return parse_system_changes(all_changes, field_details_by_name, column_lookup, actor)
    else:
        return parse_model_changes(all_changes['model_changes'], field_details_by_name, column_lookup, actor)

def parse_system_changes(all_changes, field_details_by_name, column_lookup, actor):
    model_changes = all_changes['model_changes']
    formated_fields = []
    previous_values = {}
    for system_change in  all_changes['system_changes']:
        performed_by = get_performed_by_parser(actor, system_change['name'])
        for change_name, change in list(system_change["changes"].items()):
            previous_val, current_val = None, None
            hsh = performed_by.copy()
            if change_name not in model_changes:
                continue
            elif change_name == 'type_fields':
                parsed_type_fields = system_type_field_parser(change, model_changes['type_fields'], previous_values, field_details_by_name, column_lookup, performed_by)
                formated_fields.extend(parsed_type_fields)
                continue
            elif change_name == 'impact':
                change_name = 'impact_name'
                previous_val, current_val = get_previous_and_current_values(change, change_name, previous_values, model_changes, 'value_text')
            elif change_name in field_details_by_name:
                previous_val, current_val = get_previous_and_current_values(change, change_name, previous_values, model_changes, 'value')
            elif change_name.replace("_id", "_name") in field_details_by_name: #default_dropdown
                change_name = change_name.replace("_id", "") + "_name"
                previous_val, current_val = get_previous_and_current_values(change, change_name, previous_values, model_changes, 'name')
            hsh.update(field_details_by_name[change_name])
            collect_asset_activity_values(hsh, [previous_val, current_val], column_lookup)
            formated_fields.append(hsh)
    return formated_fields

def system_type_field_parser(type_fields, model_type_field_changes, previous_values, field_details_by_name, column_lookup, performed_by):
    formated_type_fields = []
    for change in type_fields:
        change_name = change['category_name'] if change['field_type'] == 'nested_field' else change['name']
        hsh = performed_by.copy()
        previous_val, current_val = None, None
        if change_name not in model_type_field_changes:
            continue
        elif 'value_text' in change:
            change_name = change_name.rsplit('_', 1)[0] + "_name"
            previous_val, current_val = get_previous_and_current_values(change, change_name, previous_values, model_type_field_changes, "value_text")
        elif change['field_type'] == 'nested_field':
            parsed_nested_fields = system_nested_field_parser(change['nested_rules'], model_type_field_changes, previous_values, field_details_by_name, column_lookup, performed_by)
            formated_type_fields.extend(parsed_nested_fields)
            previous_val, current_val = get_previous_and_current_values(change, change_name, previous_values, model_type_field_changes, 'value')
        elif change['field_type'] == 'custom_checkbox':
            previous_val, current_val = get_previous_and_current_values(change, change_name, previous_values, model_type_field_changes, 'value')
            if type(previous_val) in [str, int]:
                previous_val = get_activity_field_value(previous_val, 'checkbox')
            if type(current_val) in [str, int]:
                previous_val = get_activity_field_value(previous_val, 'checkbox')
        elif change_name in field_details_by_name:
            previous_val, current_val = get_previous_and_current_values(change, change_name, previous_values, model_type_field_changes, 'value')
        
        hsh.update(field_details_by_name[change_name])
        collect_asset_activity_values(hsh, [previous_val, current_val], column_lookup)
        formated_type_fields.append(hsh)
    return formated_type_fields

def system_nested_field_parser(nested_fields, model_type_field_changes, previous_values, field_details_by_name, column_lookup, performed_by):
    formated_nested_fields = []
    for nested_field in nested_fields:
        change_name = nested_field['name']
        if change_name not in model_type_field_changes:
            continue
        hsh = performed_by.copy()
        previous_val, current_val = get_previous_and_current_values(nested_field, change_name, previous_values, model_type_field_changes, 'value')
        hsh.update(field_details_by_name[change_name])
        collect_asset_activity_values(hsh, [previous_val, current_val], column_lookup)
        formated_nested_fields.append(hsh)
    return formated_nested_fields


def get_previous_and_current_values(change, change_name, previous_values, model_changes, value_field):
    previous_val = None
    if change_name in previous_values:
        previous_val = previous_values[change_name]
    else:
        # As the type_field is not follow the same structure
        if(isinstance(dig(model_changes, change_name, 1), list)):
            previous_val = dig(model_changes, change_name, 1, 0)
        else:
            previous_val = dig(model_changes, change_name, 0)
    previous_values[change_name] = change[value_field]
    return [previous_val, previous_values[change_name]]
    
def parse_model_changes(model_changes, field_details_by_name, column_lookup, actor):
    performed_by = get_performed_by_parser(actor, None)
    formated_type_fields = asset_activities_fields_parser(model_changes, field_details_by_name, column_lookup, performed_by)
    formated_type_fields.extend(asset_activities_fields_parser(dig(model_changes, 'type_fields'), field_details_by_name, column_lookup, performed_by))
    return formated_type_fields

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

def asset_activities_fields_parser(all_changes, field_details_by_name, column_lookup, performed_by):
    formated_type_fields = []
    if all_changes is not None:
        for change_name, change in list(all_changes.items()):
            if(isinstance(dig(change, 1), list)):
                change = change[1]
            field_details = field_details_by_name.get(change_name)
            if field_details is None or None in [field_details.get('action_id'), field_details.get('field_type'), field_details.get('col_type')]:
                continue
            hsh = performed_by.copy()
            hsh.update(field_details)
            collect_asset_activity_values(hsh, change, column_lookup)
            formated_type_fields.append(hsh)
    return formated_type_fields

def collect_asset_activity_values(hsh, change, column_lookup):
    if hsh['col_type'] in column_lookup:
        hsh['from_value'] = get_activity_field_value(change[0], hsh['col_type'])
        hsh['to_value'] = get_activity_field_value(change[1], hsh['col_type'])
        hsh['from_column_name'] = "from_%s"%(column_lookup[hsh['col_type']])
        hsh['to_column_name'] = "to_%s"%(column_lookup[hsh['col_type']])
        hsh['from_value_string'] = None if hsh['from_value'] is None else str(hsh['from_value'])
        hsh['to_value_string'] = None if hsh['to_value'] is None else str(hsh['to_value'])

def get_activity_field_value(value, field_type):
    if value is None:
        return value
    elif field_type == "date_only":
        return str(arrow.get(value).format('YYYY-MM-DD'))
    elif field_type == "date":
        return to_utc_value(value)
    elif field_type == "checkbox":
        return bool_data(value)
    elif field_type == "number":
        return float(value)
    elif field_type in ["integer", "bigint"]:
        return int(value)
    elif field_type in ["text", "dropdown"]:
        return unescape_string(value)

def bool_data(value):
    if type(value) in [str, int]:
        value = int(value) == 1
    return value

def unescape_string(string_value):
    if type(string_value) != str:
        string_value = str(string_value)
    return html.unescape(string_value)[:255]

def to_utc_value(iso_time):
    try:
        try:
            if iso_time is None:
                return iso_time
            return str(arrow.get(parser.parse(iso_time)).to('UTC').format('YYYY-MM-DD HH:mm:ss'))
        except:
            return str(arrow.get(parser.parse(iso_time)).format('YYYY-MM-DD HH:mm:ss'))
    except:
        return None