結尾為test的csv為中型測資
可用於測試重製性。

three開頭的測資只有三個電影，
用於測試電影cosine Sim的正確性。

可直接用excel打開註記名稱為此處有手算結果的excel檔案，得知three_rating之cosine sim 
會直接符合另一資料夾ratings_three_result的輸出，因此正確性得以保障。

Ps: 因為cosine simialrity 的原始測資ml-lastest-small輸出會超過github限制之25mb，因此，只在程式部分留下匯出的code，請依照自己路徑進行修改，已全部驗證為正確輸出。