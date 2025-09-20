# Write code below 💖

sent_message = "Shouldn't have sent that"

with open("sent_message.txt", "w") as file:
  file.write(sent_message)

with open("sent_message.txt", "r+") as file:
  original_message = file.read()
  file.seek(0)

unsent_message = "This is the unsent message"  

file.truncate(len(unsent_message))

file.write(unsent_message)

print("Original Message", original_message)
print("Unsent Message", unsent_message)

file.close()