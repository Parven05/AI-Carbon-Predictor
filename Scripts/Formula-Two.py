import Orange.data as orangedpc

Input_Data = orangedpc.table_to_frame(in_data)
domain_names = [attr.name for attr in in_data.domain.attributes]

multiplied_values = Input_Data[domain_names[1]] * Input_Data[domain_names[2]]

Input_Data['Total Carbon Emissions'] = multiplied_values

print(Input_Data)

out_data = orangedpc.table_from_frame(Input_Data)

print(out_data)