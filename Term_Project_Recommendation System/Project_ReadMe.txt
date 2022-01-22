本專案目標為

1. 完全使用MapReduce方式，並完全使用使用底層資料結構RDD自行搭建算法，在不使用外部Package前提，撰寫推薦系統，以達技術上創新與客製化地解決問題。


2. 建立item- based recommendation，並進行演算法設計- BaseLine Redefinition


3. 解決問題:

(3-1) 本專案為Mining of Massive Data 技術應用之一，可解決實務上巨量數據、稀疏(Sparse)之情境下，針對data streaming 去做推薦系統與預測使用者評分。

(3-2) 因為指使用底層架構與資料結構，並未使用外來package與model- based算法，該算法設計與其他算法具有高度的擴充性、延展。

(3-3) 為item- based recommendation 設計，此外，達成技術之創新與自行定義算法的附加優勢。


4. 巨量數據測資提供檔ml-lastest，含有rating 19萬部不同電影與600多位不同user構成之評分紀錄，該數據為稀疏，並附有電影相關標籤(tags)與(categories) csv file.
此外，額外提供小型測資於檔案addition-testing-data folder中，附有3類測資，可達不同測試目標，詳見資料夾。


5. 該專案受到教授與助教好評，屬於完成度高之專案，後續仍能以此為基礎進行開發，附上證明如附檔。


# 更動項目log:
Started at 2022/12/25 20:30

1. (Completed)改動ID為數字，節省內存
    - (Designed at 12/25 20:30)


2. (Completed)確定cosin_sim = numerator_sum.leftOuterJoin(denominator_formatted) failed原因不是超時，而是partition設定問題
   -  利用設定master( local[4]) 取代原本的master( local*)，資料分太細，crashed
   - (Designed at 12/25 16:30)
   
   
3. (Completed) 重新設計分母取代卡式積的可能性? 
    - (1) 不! 我們應該當分子為0 或是不存在該關係時，直接返回cosine為0? Nope 無法
    - (2) 分子的RDD key先.leftjoin分母((mv1, mv2), rating))，這樣分子不存在的部分之後就不用跟分子join，直接大幅減少分母的row數
          Done
          
          
4. (Completed) 
    - 發現Output 有很多是成對的，例如是 ((1,2),0.33), ((2,1),0.33)這些是不需要的，有什麼辦法讓我們一開始就不會要計算算同樣的關係?
        有，先各自filter
    - 當mv_id 相等時，不用計算，因為cosine必定為1，不列出比較
    
    
    
5. (Completed) cosine similarity 顯示時會有同4點的問題，如何將相同關係的movie- movie只留下唯一一個，並去除自己對自己的關係ex.(1,1)?
   關鍵字: 顯示優化  
   
   - (Designed at 12/25 23:00)
6. (Completed)執行第三次real data 計算(12/25 23:00  )
   - 會crashed
   
7. (Completed)已經利用pandas算出item- based的 相關係數， 可以之後當作欄位corr送進去train
8. (Completed)已經利用pyspark mllib利用ALS 訓練， 可利用該結果當作欄位ALS送進去train

9. (Completed)重新確定item based算法是否正確


10. (Completed) 額外用sklearn依照item based要求設計出推薦系統了，想辦法將其重寫成RDD mapreduce算法
 - (Designed at 12/28 01:30)
11. (Completed) 重要更動去除原先設計的normalized算法: item based 算normalized cosine可能導致原先存在cosine dis變成不存在 '0'

12. (Completed)完工 不確定推薦分數是否正確 - (Designed at 12/27 20:55)

13. (Ongoing) 確定用real data可以跑得動 (創新文件跑) 

- 卡在leftOuterJoin , 進行優化 
- (Designed at 12/29 5:30 排除)


14. (Pending)block 3常常用run all會error，要手動，原因不明

15. (Completed) Socket overtime  setting
-  (Designed at 12/29 6:45 排除)


16. 論文連結:
https://www.ra.ethz.ch/cdstore/www10/papers/pdf/p519.pdf

17. (Completed) 進算法重新設計，完成到分子分母主測資能跑
-  (Designed at 12/30 00:45 排除)
18. (Completed) 進行將分子測資重新partition，但是不shuffle，完成partition num調整
-  (Designed at 12/31 03:13 排除)

19. (Completed) Part1完全可以在local運行

20. (Completed) 重寫cosine denominator算法，優化成原先1/3耗時，並確保Part I結果完全不會time out, Error
-  (Designed at 01/04 11:45 )

21. (Completed) 利用AWS EMR運行 Part II okay
-  (Designed at 01/04 14:35 )

22. (Completed) 驗算Part I 
-  (Designed at 01/05 03:05 )

23. (Completed)RePartition Testing
-  (Designed at 01/05 15:00 )

24. (Completed)推薦系統部分重構

- (Designed at 01/05 18:14 )

25.(Completed) Baseline Algorithm Refined

達成更高預測準確度。

- (Designed at 01/05 21:30 )

26.(Completed) Efficiency Boost (Repartition)

達成不需要AWS也能在本地端運行全部程式碼，並僅使用partition 8*8 的大小運算，
大幅降低內存成本與socket耗時。

- (Designed at 01/05 23:30 )