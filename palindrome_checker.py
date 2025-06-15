def is_palindrome(word):
    return word == word[::-1]

# Example usage
words = ["radar", "hello", "level", "world", "madam"]
for word in words:
    print(f"{word}: {'Palindrome' if is_palindrome(word) else 'Not a palindrome'}")
