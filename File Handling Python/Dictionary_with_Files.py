# Write code below 💖

liked_songs = {
              "Bad Habits": "Ed Sheeran",
              "I'm Just Ken": "Ryan Gosling",
              "Mastermind": "Taylor Swift",
              "Uptown Funk": "Mark Ronson ft. Bruno Mars",
              "Ghost": "Justin Bieber"
}

def write_liked_songs_to_file(liked_songs,file_name):
  with open(file_name, "w") as file:
    file.write("Liked Songs:\n")
    for song, artist in liked_songs.items():
      file.write(f"{song} by {artist}\n")
  print(f"Successfully added Liked songs to {file_name}")    


# This block will only run when the script is executed directly
if __name__ == "__main__":
    # Define the name for your output file
    output_filename = "my_favorite_songs.txt"
    # Call the function with both required arguments
    write_liked_songs_to_file(liked_songs, output_filename)
