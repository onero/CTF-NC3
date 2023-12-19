+++
title = 'In My Prime'
date = 2023-12-17T20:37:16+01:00
+++

## Challenge Name:

In My Prime

## Category:

Misc

## Challenge Description:

Du bliver givet et primtal `N` og skal inden for 3 sekunder udføre følgende tre beregninger og svare med summen af resultaterne:

1. For hvert 2. primtal fra `N` ned til 0: Udregn summen af det mest betydende og mindst betydende ciffer. Læg resultaterne sammen.
2. For hvert 3. primtal fra `N` ned til 0: Udregn tværsummen af primtallet i base 7. Læg resultaterne sammen.
3. For hvert 5. primtal fra `N` ned til 0: Lad `p1` være dette primtal og `p2` det nærmeste mindre primtal. Udregn `(p1 * p2) mod 31337` og tæl antallet af ulige cifre. Læg resultaterne sammen.

**Eksempel:**

```python
Givet N = 23:

primtal = [2,  3,  5,  7, 11, 13, 17, 19, 23]

1) [23, 17, 11, 5, 2]   - Hvert 2. primtal
2) [23, 13, 5]          - Hvert 3. primtal
3) [23, 7]              - Hvert 5. primtal


1) 2+3 + 1+7 + 1+1 + 5+5 + 2+2 = 29

2) base_7(23) = 32 -> 3 + 2  =  5
   base_7(13) = 16 -> 1 + 6  =  7
   base_7(5)  =  5 -> 5      =  5
                             -----
                               17

3) 23*19 mod 31337 = 437 -> 2
     7*5 mod 31337 =  35 -> 2
                     --------
                            4

Svaret er derfor: 29 + 17 + 4 = 50


      N |   Svar
--------+-------
     23 |     50
     97 |    178
    997 |   1434
 549979 | 509053
```

## Approach

### Let's break down the problem statement:

```text
Upon receiving a prime number N, we needed to execute and sum the results of three separate calculations:

Sum of Digits for Every Second Prime:
For every second prime number counting down from N to 0,
calculate the sum of the most and least significant digits.

Cross Sum in Base 7 for Every Third Prime:
For every third prime number from N to 0,
determine the cross sum (sum of digits) of the prime number when converted to base 7.

Modular Multiplication for Every Fifth Prime:
For every fifth prime number from N, along with the nearest smaller prime,
compute (p1 \* p2) mod 31337 and count the number of odd digits in the result.

With N = 23 as an example, the challenge seemed straightforward,
but the devil was in the details - the three-second time limit!
```

### Initial Approach and Challenges

I developed a script to test if the range of the primes had a lower and upper bound, which revealed that the challenge numbers ranged between 70 million and 100 million, which meant dealing with approximately 1.3 million primes.

```python
import socket
from collections import Counter

def get_question_and_number():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('inmyprime.nc3', 3119))
        data = s.recv(1024).decode('utf-8')

        # Extract the last line from the response
        lines = data.strip().split('\n')
        last_line = lines[-1].strip() if lines else ""

        # Ensure it's a valid integer
        try:
            question_number = int(last_line)
        except ValueError:
            question_number = None

    return question_number

def main():
    # Store numbers and their occurrences
    number_counter = Counter()

    # Track lowest and largest numbers
    lowest_number = float('inf')
    largest_number = float('-inf')

    # Make 10_000 calls
    for i in range(10_000):
        question_number = get_question_and_number()

        if question_number is not None:
            print(f"Call {i + 1}: Received question: {question_number}")

            # Count the occurrences
            number_counter[question_number] += 1

            # Update lowest and largest numbers
            lowest_number = min(lowest_number, question_number)
            largest_number = max(largest_number, question_number)

    # Find numbers asked more than once
    duplicates = {num: count for num, count in number_counter.items() if count > 1}

    print(f"\nFrom 1000 calls, the following numbers were asked more than once: {duplicates}")
    print(f"The lowest number asked: {lowest_number}")
    print(f"The largest number asked: {largest_number}")

if __name__ == "__main__":
    main()
```

Based on this knowledge, my first approach was to research the best way to efficiently compute up to 100M primes!
I came across "The Sieve of Eratosthenes", upon which I based the following implementation

```python
import time
import numpy as np

# https://www.geeksforgeeks.org/sieve-of-eratosthenes/
def compute_primes_up_to_limit_with_sieve_of_eratosthenes(n):
    x = np.ones((n+1,), dtype=bool)
    x[0] = False
    x[1] = False
    for i in range(2, int(n**0.5)+1):
        if x[i]:
            x[2*i::i] = False

    primes = np.where(x)[0][::-1]  # In reverse order, so largest is first index!
    return primes

# Extract every second prime, beginning with first number of collection!
def extract_every_second_prime(prime_numbers):
    return prime_numbers[0::2]

# Extract every second prime, beginning with third number of collection!
def extract_every_third_prime(prime_numbers):
    return prime_numbers[0::3]

# Summing up the most and least significant digits of each prime number
# So with 23 as prime example we would get this array with every second prime
#[23, 17, 11, 5, 2]
#Based on that the sum would be calculated like so
#2+3 + 1+7 + 1+1 + 5+5 + 2+2 = 29
def sum_most_and_least_significant(prime_array):
    total_sum = 0
    for num in prime_array:
        num_str = str(num)
        if len(num_str) == 1:
            total_sum += num + num
        else:
            total_sum += int(num_str[0]) + int(num_str[-1])
    return total_sum

def decimals_to_base_7(decimals):
    base_7_results = []

    for decimal_number in decimals:
        result = ""

        while decimal_number > 0:
            remainder = decimal_number % 7
            result = str(remainder) + result
            decimal_number //= 7

        base_7_results.append(int(result) if result else 0)

    return base_7_results

# https://stackoverflow.com/questions/14939953/sum-the-digits-of-a-number-python
def sum_of_digits(number):
    return sum(int(digit) for digit in str(number))

# Calculate the sum of digits of every base_7 representation
# Example
#  base_7(23) = 32 -> 3 + 2  =  5
#  base_7(13) = 16 -> 1 + 6  =  7
#  base_7(5)  =  5 -> 5      =  5
def calculate_base_7_sums(decimals):
    return [sum_of_digits(base_7_result) for base_7_result in decimals]

def solve_first_calculation(prime_numbers):
    # Extract primes in orders (beginning with first!)
    every_second_prime = extract_every_second_prime(prime_numbers)
    # Calculate most and least significant sums of every second prime
    return sum_most_and_least_significant(every_second_prime)

def solve_second_calculation(prime_numbers):
    # Extract primes in orders (beginning with third!)
    every_third_prime = extract_every_third_prime(prime_numbers)
    # Calculate base_7 representations of every third prime
    base_7_results = decimals_to_base_7(every_third_prime)
    # Calculate the sum of digits of every base_7 representation
    base_7_sums = calculate_base_7_sums(base_7_results)
    # Calculate the sum of all base_7 sums
    return sum(base_7_sums)

# For every fifth prime number from N down to 0: Let p1 be this prime number and p2 the nearest smaller prime number.
# Calculate (p1 * p2) mod 31337 and count the number of odd digits.
# Add up the results.
def solve_third_calculation(primes):
    sum_of_odd_digits = 0

    # For every fifth prime number, along with its next lower prime number
    # Implement loop that starts with first and takes every fifth prime number
    for i in range(0, len(primes) -1, 5):
        # Calculate the product of the two primes modulo 31337
        result = primes[i] * primes[i + 1] % 31337
        # Count the number of odd digits in the product
        odd_digit_count = sum(1 for digit in str(result) if int(digit) % 2 == 1)
        sum_of_odd_digits += odd_digit_count

    return sum_of_odd_digits

def calculate_results(prime_numbers):
    result_a = solve_first_calculation(prime_numbers)
    result_b = solve_second_calculation(prime_numbers)
    result_c = solve_third_calculation(prime_numbers)
    return result_a + result_b + result_c

def main():
    start_time = time.time()
    print("Computing all primes up to 100 million. This may take a while...")

    prime_limit = 100000000
    all_primes = compute_primes_up_to_limit_with_sieve_of_eratosthenes(prime_limit)

    end_time = time.time()
    print(f"Computed all primes up to 100 million in {end_time - start_time:.2f} seconds.")

    while True:
        try:
            question = int(input("Enter the question (or enter -1 to exit): "))
            if question == -1:
                break

            if question > prime_limit or question < 0:
                print("Please enter a number between 0 and 100,000,000.")
                continue

            relevant_primes = all_primes[all_primes <= question]

            calculation_start_time = time.time()
            result = calculate_results(relevant_primes)
            calculation_end_time = time.time()

            print(f"Result for N = {question}: {result}")
            print(f"Calculation time: {calculation_end_time - calculation_start_time:.2f} seconds.")

        except ValueError:
            print("Invalid input. Please enter a valid integer.")

if __name__ == "__main__":
    main()

> Output:
Computing all primes up to 100 million. This may take a while...
Computed all primes up to 100 million in 0.74 seconds.
Enter the question (or enter -1 to exit): 99043661
Result for N = 99043661: 83814368
Calculation time: 10.67 seconds.
```

However, it quickly became evident that Python's execution time exceeded the allotted three seconds, indicating the necessity for a pre-calculated approach!

### Strategy and Solution Development

To tackle this, I developed a two-pronged strategy, involving a self-learning Python script and a bruteforce version in Rust:

1. The "Self-Learning" script in Python would:

- Request a question
- Lookup the result in the pre-calculated cache and respond with a known result
- If not pre-calculated, it would compute the solution.
- Submit the answer, despite being late.
- Add the result to a cache for future reference.

This method ensured a gradually growing cache, improving our chances of encountering a known question.

```python
import sys
import os
import pickle
import numpy as np
import socket

def compute_primes_up_to_limit_with_sieve_of_eratosthenes(n):
    # ... [same as in previous example] ...

def extract_every_second_prime(prime_numbers):
    # ... [same as in previous example] ...

def extract_every_third_prime(prime_numbers):
    # ... [same as in previous example] ...

def sum_most_and_least_significant(prime_array):
    # ... [same as in previous example] ...

def decimals_to_base_7(decimals):
    # ... [same as in previous example] ...

def sum_of_digits(number):
    # ... [same as in previous example] ...

def calculate_base_7_sums(decimals):
    # ... [same as in previous example] ...

def solve_first_calculation(prime_numbers):
    # ... [same as in previous example] ...

def solve_second_calculation(prime_numbers):
    # ... [same as in previous example] ...

def solve_third_calculation(primes):
    # ... [same as in previous example] ...

def calculate_results(prime_numbers):
    # ... [same as in previous example] ...


# Load pre-calculated results from file, written in pickle format
def load_results(filename):
    print("Checking if we have pre-calculated results...")
    if os.path.exists(filename):
        print("We do! Loading pre-calculated results from file...")
        with open(filename, 'rb') as file:
            results = pickle.load(file)
            print("Done loading!... ")
            # Let's be a bit cocky if we have a lot of results already computed...
            if len(results) > 100:
                attempts = len(results)
                print("Jesus, we have {} results already computed... not your first time trying this huh!? :D".format(attempts))
            return results
    else:
        print("No pre-calculated results found!")
        return {}

def get_question_from_server(socket_connection):
    data = socket_connection.recv(1024).decode('utf-8')

    # Extract the last line from the response
    lines = data.strip().split('\n')
    last_line = lines[-1].strip() if lines else ""

    # Ensure it's a valid integer
    try:
        question_number = int(last_line)
    except ValueError:
        print("Error while parsing question number!")
        question_number = None

    print(f"Received question: {question_number}")
    return question_number

def submit_answer(socket_connection, answer):
    socket_connection.sendall(str(answer).encode('utf-8'))

    # Receive and print the server's reply
    data = socket_connection.recv(1024).decode('utf-8')
    print(f"Server's reply: {data}")
    return data

def challenge_solved(response):
    challenge_timeout_answer = "Sorry, too slow. Please try again."
    return response != challenge_timeout_answer and response != ""

def main():
    server_address = ('inmyprime.nc3', 3119)
    challenge_wrong_answer_message = "Nope, wrong answer. Please try again."
    result_not_pre_calculated_message = "Result not pre-calculated :(... Let's calculate it now!"
    results = {}
    attempts = 0

    print("Welcome to Adamino's automagic prime solver! Let's go!")

    # Load pre-calculated results from file
    results_filename = 'results.pkl'
    results = load_results(results_filename)
    attempts = len(results)

    # Request prime number from server and provide response
    response_from_server = ""

    while not challenge_solved(response_from_server):
        attempts += 1
        print("\nAttempt {}...".format(attempts))

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(server_address)

            # Get the question number from the server
            limit = get_question_from_server(s)

            # Check if the answer is in the results
            result = results.get(limit, result_not_pre_calculated_message)

            # If the result is not pre-calculated, calculate it now
            if result == result_not_pre_calculated_message:
                print(result_not_pre_calculated_message)

                precalculated_primes = compute_primes_up_to_limit_with_sieve_of_eratosthenes(limit)

                result = calculate_results(precalculated_primes)

                # Add the result in the results dictionary
                results[limit] = result

                response_from_server = submit_answer(s, result)

                # Save the results to file (should happen after submitting to server for faster execution!)
                with open(results_filename, 'wb') as file:
                    pickle.dump(results, file)

                print("The result is: {} and was added to known results!".format(result))
            else:
                # Send the answer to the server
                response_from_server = submit_answer(s, result)

        if response_from_server == challenge_wrong_answer_message:
            print("Oh noes! Wrong answer! How could this happen!? :( Stopping process, because you need to fix this!")
            sys.exit(1)

    print(f"\nOMFG.. this print either means that something bad happened... or YOU'RE DA FUCKING MAN!: {response_from_server}")

if __name__ == "__main__":
    main()
```

![Automagic Prime Solver](images/automagic-prime-solver.png)

2. My second apporach was to "simply" Compute-All-Solutions in Rust (being one of the faster languages):

Running on a dedicated server, this script aimed to pre-calculate solutions for all possible primes within the range.
Given the number of primes involved, this was a time-intensive process...

```rust
use std::fs;
use std::time::Instant;

// https://www.geeksforgeeks.org/sieve-of-eratosthenes/
fn sieve_of_eratosthenes(n: usize) -> Vec<usize> {
    let mut x = vec![true; n + 1];
    x[0] = false;
    x[1] = false;
    for i in 2..=(n as f64).sqrt() as usize {
        if x[i] {
            x[2 * i..=n].iter_mut().step_by(i).for_each(|v| *v = false);
        }
    }

    let primes: Vec<usize> = x.into_iter().enumerate().filter_map(|(i, is_prime)| if is_prime { Some(i) } else { None }).rev().collect();
    primes
}

// Extract every second prime, beginning with first number of collection!
fn extract_every_second_prime(prime_numbers: &[usize]) -> Vec<usize> {
    prime_numbers.iter().cloned().step_by(2).collect()
}

fn extract_every_third_prime(prime_numbers: &[usize]) -> Vec<usize> {
    prime_numbers.iter().cloned().step_by(3).collect()
}

// Summing up the most and least significant digits of each prime number
// So with 23 as prime example we would get this array with every second prime
// [23, 17, 11, 5, 2]
// Based on that the sum would be calculated like so
// 2+3 + 1+7 + 1+1 + 5+5 + 2+2 = 29
fn sum_most_and_least_significant(prime_array: &[usize]) -> usize {
    let total_sum = prime_array.iter().map(|&num| {
        let num_str = num.to_string();
        if num_str.len() == 1 {
            num + num
        } else {
            num_str.chars().next().unwrap().to_digit(10).unwrap() as usize
                + num_str.chars().last().unwrap().to_digit(10).unwrap() as usize
        }
    }).sum();

    total_sum
}

fn decimals_to_base_7(decimals: &[usize]) -> Vec<usize> {
    decimals.iter().cloned().map(|decimal_number| {
        let mut result = Vec::new();
        let mut num = decimal_number;

        while num > 0 {
            let remainder = num % 7;
            result.push(remainder);
            num /= 7;
        }

        result.reverse();
        if result.is_empty() { 0 } else { result.iter().fold(0, |acc, &x| acc * 10 + x) }
    }).collect()
}

// https://stackoverflow.com/questions/14939953/sum-the-digits-of-a-number-python
fn sum_of_digits(number: usize) -> usize {
    number.to_string().chars().map(|c| c.to_digit(10).unwrap() as usize).sum()
}

// Calculate the sum of digits of every base_7 representation
// Example
// base_7(23) = 32 -> 3 + 2 = 5
// base_7(13) = 16 -> 1 + 6 = 7
// base_7(5)  = 5 -> 5 = 5
fn calculate_base_7_sums(decimals: &[usize]) -> Vec<usize> {
    decimals.iter().cloned().map(|base_7_result| sum_of_digits(base_7_result)).collect()
}

fn solve_first_calculation(prime_numbers: &[usize]) -> usize {
    // Extract primes in orders (beginning with first!)
    let every_second_prime = extract_every_second_prime(prime_numbers);
    // Calculate most and least significant sums of every second prime
    sum_most_and_least_significant(&every_second_prime)
}

fn solve_second_calculation(prime_numbers: &[usize]) -> usize {
    // Extract primes in orders (beginning with third!)
    let every_third_prime = extract_every_third_prime(prime_numbers);
    // Calculate base_7 representations of every third prime
    let base_7_results = decimals_to_base_7(&every_third_prime);
    // Calculate the sum of digits of every base_7 representation
    let base_7_sums = calculate_base_7_sums(&base_7_results);
    // Calculate the sum of all base_7 sums
    base_7_sums.iter().sum()
}

// For every fifth prime number from N down to 0: Let p1 be this prime number and p2 the nearest smaller prime number.
// Calculate (p1 * p2) mod 31337 and count the number of odd digits.
// Add up the results.
fn solve_third_calculation(primes: &[usize]) -> usize {
    let sum_of_odd_digits = primes
        .iter()
        .step_by(5)
        .filter_map(|&p1| primes.iter().cloned().find(|&p2| p2 < p1).map(|p2| (p1, p2)))
        .map(|(p1, p2)| {
            let result = (p1 * p2) % 31337;
            result.to_string().chars().filter(|&c| c.to_digit(10).unwrap() % 2 == 1).count()
        })
        .sum();

    sum_of_odd_digits
}

fn calculate_results(prime_numbers: &[usize]) -> usize {
    let result_a = solve_first_calculation(prime_numbers);
    let result_b = solve_second_calculation(prime_numbers);
    let result_c = solve_third_calculation(prime_numbers);

    result_a + result_b + result_c
}

fn main() {
    // Pre-calculate all primes up to theoretical limit
    let precalculated_primes = sieve_of_eratosthenes(100_000_000);

    // Check if results are precalculated, if not, calculate them
    let start_time = Instant::now();
    let result = calculate_results(&precalculated_primes);
    let end_time = Instant::now();

    println!(
        "Time to calculate result: {:.5} seconds",
        (end_time - start_time).as_secs_f64()
    );
    println!("The result is: {}", result);
}

```

### The Breakthrough

As the Python script's cache grew to 6,000 pre-calculated results, I developed a "Lucky Prime" script that would:

- Request a question
- Check the cache for a pre-calculated answer.
- Disconnect if the answer wasn't in the cache, saving the question for later.
- Retry until it hit a known question.

![Lucky Prime](images/lucky-prime.png)
Finally, on the 8,876th attempt, success was achieved! The "Lucky Prime" script cracked the challenge first, closely followed by our self-learning Python script.

In the end first the lucky_prime solved the challenge and on attempt 8.876 the self-learning script also succeeded!

## Flag

```text
NC3{th3_numb3rs_wh4t_d0_th3y_m3an?}
```

## Reflections and Learnings

This challenge was a testament to the importance of optimization and strategy in problem-solving. It underscored the need for efficient computation, especially when dealing with large datasets and tight time constraints. The experience was a valuable lesson in balancing brute-force approaches with intelligent caching and pre-calculation strategies.

Overall, "In My Prime" was not just a test of mathematical prowess but also a challenge of computational efficiency and algorithmic thinking.

In your write-up, make sure to include any specific code snippets or algorithms you found particularly interesting or challenging. Personal anecdotes or moments of realization can also add a great narrative quality to the write-up.
