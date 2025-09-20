import java.util.Scanner;

public class CesarCipher {
    public static String encrypt(String text, int shift) {
    StringBuilder result = new StringBuilder();

    for (char character : text.toCharArray()) {
        if (Character.isLetter(character)) {
            char base = Character.isLowerCase(character) ? 'a' : 'A';
            // This formula correctly handles both positive and negative shifts
            char shifted = (char) ((((character - base + shift) % 26) + 26) % 26 + base);
            result.append(shifted);
        } else {
            result.append(character);
        }
    }

    return result.toString();
}

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter text to encrypt: ");
        String text = scanner.nextLine();



        System.out.print("Enter shift value: ");
        int shiftKey = scanner.nextInt();

        String encrypted = encrypt(text, shiftKey);
        System.out.println("Encrypted text: " + encrypted);

        // Close the scanner to avoid resource leaks
        scanner.close();
    }
}
