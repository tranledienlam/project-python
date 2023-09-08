# import items_path
import categories
import output
import items

## Output category. Note, delete old file
cats_parent = categories.get_children()
output.to_csv(input_df=cats_parent, output_csv='categories.csv')

## Output SUB_category. Note, delete old file
cats_children = categories.get_children()
output.to_csv(input_df=cats_children, output_csv='subcategories.csv')


# path = 'Áo-Khoác-cat.11035567.11035568'
# itemsDetail = items.detail_cat(path, page=1)
# # print(itemsDetail)
# # itemsDetail = [
# #     {'ID': 1, 'Name': 'Alice'},
# #     {'ID': 2, 'Name': 'Bob'},
# #     {'ID': 3, 'Name': 'Charlie'},
# # ]
# output.to_csv(input_df=itemsDetail,output_csv='products.csv')