class Solution(object):
    def maximumSubarraySum(self, nums, k):
        freq = {}
        l = 0
        curr_sum = 0
        max_sum = 0
        distinct_count = 0

        for r in range(len(nums)):

            # Add nums[r] to hashmap
            old = freq.get(nums[r], 0)
            freq[nums[r]] = old + 1
            curr_sum += nums[r]

            if old == 0:
                distinct_count += 1     # new distinct element
            elif old == 1:
                distinct_count -= 1     # becomes non-distinct

            # Shrink window if size > k
            while r - l + 1 > k:
                old = freq[nums[l]]
                freq[nums[l]] = old - 1
                curr_sum -= nums[l]

                if old == 2:
                    distinct_count += 1   # goes from freq 2 → 1, becomes distinct again
                elif old == 1:
                    distinct_count -= 1   # goes from freq 1 → 0, removed from distinct

                if freq[nums[l]] == 0:
                    del freq[nums[l]]

                l += 1

            # Valid window: size k AND all elements are distinct
            if r - l + 1 == k and distinct_count == k:
                max_sum = max(max_sum, curr_sum)

        return max_sum