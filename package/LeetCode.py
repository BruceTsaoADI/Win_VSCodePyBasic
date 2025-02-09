class Solution:
    def minimumMountainRemovals(self, nums: list[int]) -> int:
        # reshape nums, record steps
        steps = 0
        while True:
            ''' remove peaks locate in both side '''
            index_peak = nums.index(max(nums))
            if index_peak == 0:
                nums.pop(0)
                steps += 1
            elif index_peak == len(nums) - 1:
                nums.pop()
                steps += 1
            else:
                break

        while True:
            # index_peak = nums.count(max(nums))
            if nums.count(max(nums)) > 1:
                nums.remove(max(nums))
                steps += 1
            else:
                break

        peak = max(nums)
        index_peak = nums.index(peak)
        nums_left = nums[:index_peak]
        nums_right = nums[index_peak+1:]
        mnt_left = []
        mnt_right = []

        nums_no_sort = nums_left
        index_min = nums.index(min(nums_no_sort))
        candidate = min(nums_no_sort)
        candidates = [candidate]
        for i in nums_no_sort[index_min:]:
            if candidate < i:
                candidates.append(i)
                candidate = i
        mnt_left = candidates

        nums_no_sort = nums_right[::-1]
        index_min = nums.index(min(nums_no_sort))
        candidate = min(nums_no_sort)
        candidates = [candidate]
        for i in nums_no_sort[index_min:]:
            if candidate < i:
                candidates.append(i)
                candidate = i
        mnt_right = candidates[::-1]

        mnt = mnt_left + [peak] + mnt_right

        return steps + ( len(nums) - len(mnt) )


solu = Solution()
# arg1 = [2,1,1,5,6,2,3,1]
# arg1 = [4,3,2,1,1,2,3,1]
# arg1 = [1,2,3,4,4,3,2,1]
arg1 = [1,16,84,9,29,71,86,79,72,12]
# arg2 = []
ans = solu.minimumMountainRemovals(arg1)
print(ans)
