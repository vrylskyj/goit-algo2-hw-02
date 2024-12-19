from typing import List, Dict, Tuple

def get_optimal_cuts(dp_table: List[int], length: int, prices: List[int]) -> List[int]:
    """Helper function to reconstruct the optimal cuts from dp table"""
    cuts = []
    remaining_length = length
    
    while remaining_length > 0:
        best_cut = 1
        for i in range(1, remaining_length + 1):
            if dp_table[remaining_length] == prices[i-1] + dp_table[remaining_length - i]:
                best_cut = i
                break
        cuts.append(best_cut)
        remaining_length -= best_cut
    
    return sorted(cuts)

def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Finds optimal cutting strategy using memoization
    """
    memo = [-1] * (length + 1)
    cuts_memo = {}

    def cut_rod(n: int) -> Tuple[int, List[int]]:
        if n == 0:
            return 0, []
        if memo[n] != -1:
            return memo[n], cuts_memo.get(n, [])

        max_profit = float('-inf')
        best_cuts = []

        for i in range(1, n + 1):
            current_profit, sub_cuts = cut_rod(n - i)
            total_profit = prices[i-1] + current_profit
            
            if total_profit > max_profit:
                max_profit = total_profit
                best_cuts = [i] + sub_cuts

        memo[n] = max_profit
        cuts_memo[n] = best_cuts
        return max_profit, best_cuts

    max_profit, cuts = cut_rod(length)
    
    return {
        "max_profit": max_profit,
        "cuts": sorted(cuts),
        "number_of_cuts": len(cuts) - 1 if cuts else 0
    }

def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Finds optimal cutting strategy using tabulation
    """
    dp = [0] * (length + 1)
    
    # Fill the dp table
    for i in range(1, length + 1):
        max_val = float('-inf')
        for j in range(i):
            max_val = max(max_val, prices[j] + dp[i - j - 1])
        dp[i] = max_val
    
    # Get the cuts that led to optimal solution
    cuts = get_optimal_cuts(dp, length, prices)
    
    return {
        "max_profit": dp[length],
        "cuts": cuts,
        "number_of_cuts": len(cuts) - 1 if cuts else 0
    }

def run_tests():
    """Function to run all tests"""
    test_cases = [
        # Test 1: Basic case
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Basic case"
        },
        # Test 2: Optimal not to cut
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Optimal not to cut"
        },
        # Test 3: All cuts of length 1
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Uniform cuts"
        }
    ]

    for test in test_cases:
        print(f"\nTest: {test['name']}")
        print(f"Rod length: {test['length']}")
        print(f"Prices: {test['prices']}")

        # Test memoization
        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print("\nMemoization result:")
        print(f"Maximum profit: {memo_result['max_profit']}")
        print(f"Cuts: {memo_result['cuts']}")
        print(f"Number of cuts: {memo_result['number_of_cuts']}")

        # Test tabulation
        table_result = rod_cutting_table(test['length'], test['prices'])
        print("\nTabulation result:")
        print(f"Maximum profit: {table_result['max_profit']}")
        print(f"Cuts: {table_result['cuts']}")
        print(f"Number of cuts: {table_result['number_of_cuts']}")

        # Verify results match
        assert memo_result['max_profit'] == table_result['max_profit'], "Profits don't match!"
        assert len(memo_result['cuts']) == len(table_result['cuts']), "Number of cuts doesn't match!"
        assert memo_result['number_of_cuts'] == table_result['number_of_cuts'], "Cut counts don't match!"

        print("\nTest passed successfully!")

if __name__ == "__main__":
    run_tests()