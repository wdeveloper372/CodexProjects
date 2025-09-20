import csv

max_sales = 0

with open('Bestseller - Sheet1.csv', 'r') as file:
    csv_reader = csv.reader(file)

    file.readline()  # Skip the header row
    
    for row in csv_reader:
        current_sales = float(row[4])


        if current_sales > max_sales:
            max_sales = current_sales
            best_selling_book = row[0]

output_file_path = 'bestseller_info.csv'
with open(output_file_path, 'w', newline='') as output_file:
  csv_writer = csv.writer(output_file)
  
  # Write header
  csv_writer.writerow(['Book', 'Author', 'Sales in Millions'])
  
  # Write best-selling book info
  csv_writer.writerow([best_selling_book[0], best_selling_book[1], best_selling_book[4]])

# Bonus: Print confirmation message
print('Bestselling info written to', output_file_path)