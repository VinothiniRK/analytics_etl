def asset_activity_type_field_by_name(type_field_properties):
    type_fields_by_name = {}
    dropdown_field_mapping = {'default_product': 'product_name', 'default_vendor': 'vendor_name', 'default_domain': 'domain_name', 'default_asset_state': 'asset_state_name'}
    for type_field in type_field_properties:
        if(None in [type_field.get('id'), type_field.get('name'), type_field.get('type'), type_field.get('col_type')]):
            continue
        name, col_type = type_field['name'], type_field['col_type']
        field_type = "Cmdb::NestedField" if type_field['type'] == "nested_nested_fields" else "Cmdb::CiTypeField"
        if type_field['type'] in dropdown_field_mapping:
            col_type, name = 'dropdown', dropdown_field_mapping[type_field['type']]
        type_fields_by_name[name] = {'action_id': type_field['id'], 'field_type': field_type, 'col_type': col_type}
    return type_fields_by_name