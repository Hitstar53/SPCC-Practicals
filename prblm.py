# Longest Substring Without Repeating Characters. Given a string, find the length of the longest substring without repeating characters.

def length_of_longest_substring(s):
    start = maxLength = 0
    usedChar = {}
    for i in range(len(s)):
        if s[i] in usedChar and start <= usedChar[s[i]]:
            start = usedChar[s[i]] + 1
        else:
            maxLength = max(maxLength, i - start + 1)
        usedChar[s[i]] = i
    return maxLength

print(length_of_longest_substring("abcabcbb"))  # Output: 3
print(length_of_longest_substring("bbbbb"))  # Output: 1
print(length_of_longest_substring("pwwkew"))  # Output: 3
print(length_of_longest_substring(""))  # Output: 0

# Median of Two Sorted Arrays. Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.

def find_median_sorted_arrays(nums1, nums2):
    A, B = nums1, nums2
    total = len(nums1) + len(nums2)
    half = total // 2
    if len(B) < len(A):
        A, B = B, A
    l, r = 0, len(A) - 1
    while True:
        i = (l + r) // 2
        j = half - i - 2
        Aleft = A[i] if i >= 0 else float('-inf')
        Aright = A[i + 1] if (i + 1) < len(A) else float('inf')
        Bleft = B[j] if j >= 0 else float('-inf')
        Bright = B[j + 1] if (j + 1) < len(B) else float('inf')
        if Aleft <= Bright and Bleft <= Aright:
            if total % 2:
                return min(Aright, Bright)
            else:
                return (max(Aleft, Bleft) + min(Aright, Bright)) / 2
        elif Aleft > Bright:
            r = i - 1
        else:
            l = i + 1
        
print(find_median_sorted_arrays([1, 3], [2]))  # Output: 2.0
print(find_median_sorted_arrays([1, 2], [3, 4]))  # Output: 2.5
print(find_median_sorted_arrays([0, 0], [0, 0]))  # Output: 0.0
print(find_median_sorted_arrays([], [1]))  # Output: 1.0
print(find_median_sorted_arrays([2], []))  # Output: 2.0


# Longest Palindromic Substring. Given a string s, return the longest palindromic substring in s.

def longest_palindrome(s):
    if len(s) == 0:
        return 0
    max_len = 1
    start = 0
    for i in range(len(s)):
        if (
            i - max_len >= 1
            and s[i - max_len - 1 : i + 1] == s[i - max_len - 1 : i + 1][::-1]
        ):
            start = i - max_len - 1
            max_len += 2
            continue
        if s[i - max_len : i + 1] == s[i - max_len : i + 1][::-1]:
            start = i - max_len
            max_len += 1
    return s[start : start + max_len]

print(longest_palindrome("babad"))  # Output: "bab"
print(longest_palindrome("cbbd"))  # Output: "bb"
print(longest_palindrome("a"))  # Output: "a"
print(longest_palindrome("ac"))  # Output: "a"