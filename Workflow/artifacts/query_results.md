# Query Results（query_wiki 節點輸出）

> 由 `validators/query.py` 自動產生：每張投影片用大綱中的關鍵詞檢索 Wiki，列出命中的節點與分數。
> draft_content 只能使用這裡列出的節點。

## Slide 1：Cryptography 101
- 關鍵詞：（不需要）
- 命中：無

## Slide 2：今天的路線圖
- 關鍵詞：教學順序, teaching approach
- **teaching-how-others-explain**（別人怎麼介紹加密演算法？（教學設計參考））score=10；來源 S13, S14, S15；依據 title/alias:教學順序; title/alias:teaching approach

## Slide 3：為什麼需要密碼學？
- 關鍵詞：密碼學, information security, Cryptography
- **intro-what-is-crypto**（密碼學是什麼？為什麼需要它？）score=23；來源 S01, S02；依據 title/alias:密碼學; body:密碼學×3; title/alias:information security; body:information security×2; title/alias:Cryptography; body:Cryptography×3
- **asym-public-key**（公開金鑰密碼學（Asymmetric / Public-Key Cryptography））score=15；來源 S02, S06, S07；依據 title/alias:密碼學; body:密碼學×2; title/alias:Cryptography; body:Cryptography×3
- **app-hybrid-tls**（密碼學在現代網路的應用：混合加密與 HTTPS／TLS 1.3）score=8；來源 S06, S10；依據 title/alias:密碼學; body:密碼學×2; body:Cryptography×1

## Slide 4：密碼學在做什麼？基本名詞
- 關鍵詞：明文, 密文, 金鑰, 加密
- **intro-terminology**（基本術語：明文、密文、金鑰、加密與解密）score=32；來源 S01, S02；依據 title/alias:明文; body:明文×3; title/alias:密文; body:密文×3; title/alias:金鑰; body:金鑰×3; title/alias:加密; body:加密×3
- **asym-public-key**（公開金鑰密碼學（Asymmetric / Public-Key Cryptography））score=17；來源 S02, S06, S07；依據 body:密文×1; title/alias:金鑰; body:金鑰×3; title/alias:加密; body:加密×3
- **sym-block-vs-stream**（區塊加密（Block Cipher）與串流加密（Stream Cipher））score=17；來源 S02, S06；依據 body:明文×1; title/alias:金鑰; body:金鑰×3; title/alias:加密; body:加密×3
- **sym-concept**（對稱式加密（Symmetric Encryption）與金鑰分配問題）score=17；來源 S02, S06；依據 body:密文×1; title/alias:金鑰; body:金鑰×3; title/alias:加密; body:加密×3
- **classical-limitations**（古典密碼的限制：金鑰空間太小與頻率分析）score=16；來源 S02, S03；依據 body:明文×3; body:密文×3; title/alias:金鑰; body:金鑰×3; body:加密×2

## Slide 5：演算法可以公開，金鑰必須保密
- 關鍵詞：Kerckhoffs, 暴力破解
- **intro-kerckhoffs**（Kerckhoffs 原則、金鑰空間與暴力破解）score=15；來源 S01, S02；依據 title/alias:Kerckhoffs; body:Kerckhoffs×3; title/alias:暴力破解; body:暴力破解×2

## Slide 6：兩個數學小工具：mod 與 XOR
- 關鍵詞：XOR, 取餘數, 模運算
- **basics-bits-xor-mod**（基礎工具：位元、位元組、十六進位、XOR 與 mod）score=21；來源 S04, S08, S13, S14；依據 title/alias:XOR; body:XOR×3; title/alias:取餘數; body:取餘數×3; title/alias:模運算
- **teaching-how-others-explain**（別人怎麼介紹加密演算法？（教學設計參考））score=4；來源 S13, S14, S15；依據 body:XOR×3; body:模運算×1

## Slide 7：第 2 章：古典密碼
- 關鍵詞：Kerckhoffs, XOR, 取餘數
- **basics-bits-xor-mod**（基礎工具：位元、位元組、十六進位、XOR 與 mod）score=16；來源 S04, S08, S13, S14；依據 title/alias:XOR; body:XOR×3; title/alias:取餘數; body:取餘數×3
- **intro-kerckhoffs**（Kerckhoffs 原則、金鑰空間與暴力破解）score=8；來源 S01, S02；依據 title/alias:Kerckhoffs; body:Kerckhoffs×3
- **sym-aes**（AES（Advanced Encryption Standard））score=5；來源 S01, S04, S06, S12；依據 body:Kerckhoffs×2; body:XOR×3
- **teaching-how-others-explain**（別人怎麼介紹加密演算法？（教學設計參考））score=4；來源 S13, S14, S15；依據 body:Kerckhoffs×1; body:XOR×3

## Slide 8：Caesar 密碼：每個字母往後移 k 位
- 關鍵詞：Caesar cipher, 凱撒密碼, 位移密碼
- **classical-caesar**（Caesar Cipher（凱撒密碼／位移密碼））score=19；來源 S02, S03；依據 title/alias:Caesar cipher; body:Caesar cipher×1; title/alias:凱撒密碼; body:凱撒密碼×1; title/alias:位移密碼; body:位移密碼×2

## Slide 9：替換密碼：把整個字母表打亂
- 關鍵詞：替換密碼, substitution cipher
- **classical-substitution**（替換密碼（Substitution Cipher）：單表、同音、多表（Vigenère））score=15；來源 S02, S03；依據 title/alias:替換密碼; body:替換密碼×2; title/alias:substitution cipher; body:substitution cipher×3

## Slide 10：多表替換：Vigenère 密碼
- 關鍵詞：Vigenère cipher, 多表替換, polyalphabetic substitution
- **classical-substitution**（替換密碼（Substitution Cipher）：單表、同音、多表（Vigenère））score=18；來源 S02, S03；依據 title/alias:Vigenère cipher; body:Vigenère cipher×1; title/alias:多表替換; body:多表替換×2; title/alias:polyalphabetic substitution

## Slide 11：換位密碼：字母不變，位置打亂
- 關鍵詞：換位密碼, transposition cipher
- **classical-transposition**（換位密碼（Transposition Cipher））score=16；來源 S02, S03；依據 title/alias:換位密碼; body:換位密碼×3; title/alias:transposition cipher; body:transposition cipher×3

## Slide 12：古典密碼怎麼被破解？
- 關鍵詞：頻率分析, frequency analysis, Kasiski
- **classical-limitations**（古典密碼的限制：金鑰空間太小與頻率分析）score=21；來源 S02, S03；依據 title/alias:頻率分析; body:頻率分析×3; title/alias:frequency analysis; body:frequency analysis×1; title/alias:Kasiski; body:Kasiski×2
- **classical-substitution**（替換密碼（Substitution Cipher）：單表、同音、多表（Vigenère））score=5；來源 S02, S03；依據 body:頻率分析×2; body:frequency analysis×1; body:Kasiski×2

## Slide 13：第 3 章：對稱式加密
- 關鍵詞：頻率分析, Kasiski, frequency analysis
- **classical-limitations**（古典密碼的限制：金鑰空間太小與頻率分析）score=21；來源 S02, S03；依據 title/alias:頻率分析; body:頻率分析×3; title/alias:Kasiski; body:Kasiski×2; title/alias:frequency analysis; body:frequency analysis×1
- **classical-substitution**（替換密碼（Substitution Cipher）：單表、同音、多表（Vigenère））score=5；來源 S02, S03；依據 body:頻率分析×2; body:Kasiski×2; body:frequency analysis×1

## Slide 14：對稱式加密：同一把金鑰鎖上也打開
- 關鍵詞：對稱式加密, symmetric encryption
- **sym-concept**（對稱式加密（Symmetric Encryption）與金鑰分配問題）score=14；來源 S02, S06；依據 title/alias:對稱式加密; body:對稱式加密×3; title/alias:symmetric encryption; body:symmetric encryption×1
- **asym-public-key**（公開金鑰密碼學（Asymmetric / Public-Key Cryptography））score=7；來源 S02, S06, S07；依據 title/alias:對稱式加密; body:對稱式加密×2

## Slide 15：對稱式加密的好處與難題
- 關鍵詞：金鑰分配問題, 對稱式加密, public key
- **asym-public-key**（公開金鑰密碼學（Asymmetric / Public-Key Cryptography））score=16；來源 S02, S06, S07；依據 body:金鑰分配問題×1; title/alias:對稱式加密; body:對稱式加密×2; title/alias:public key; body:public key×3
- **sym-concept**（對稱式加密（Symmetric Encryption）與金鑰分配問題）score=15；來源 S02, S06；依據 title/alias:金鑰分配問題; body:金鑰分配問題×2; title/alias:對稱式加密; body:對稱式加密×3
- **asym-key-exchange**（Diffie–Hellman 金鑰交換（Key Exchange））score=8；來源 S02, S07, S08, S10；依據 body:金鑰分配問題×1; title/alias:public key; body:public key×2

## Slide 16：兩種做法：區塊加密與串流加密
- 關鍵詞：區塊加密, 串流加密
- **sym-block-vs-stream**（區塊加密（Block Cipher）與串流加密（Stream Cipher））score=16；來源 S02, S06；依據 title/alias:區塊加密; body:區塊加密×3; title/alias:串流加密; body:串流加密×3
- **teaching-how-others-explain**（別人怎麼介紹加密演算法？（教學設計參考））score=5；來源 S13, S14, S15；依據 body:區塊加密×3; body:串流加密×2
- **mode-ctr**（CTR（Counter）模式）score=4；來源 S05；依據 body:區塊加密×3; body:串流加密×1

## Slide 17：電腦裡的資料：位元、位元組、十六進位
- 關鍵詞：位元組, 十六進位, byte
- **basics-bits-xor-mod**（基礎工具：位元、位元組、十六進位、XOR 與 mod）score=24；來源 S04, S08, S13, S14；依據 title/alias:位元組; body:位元組×3; title/alias:十六進位; body:十六進位×3; title/alias:byte; body:byte×3
- **sym-aes**（AES（Advanced Encryption Standard））score=6；來源 S01, S04, S06, S12；依據 body:位元組×3; body:byte×3

## Slide 18：現實中的對稱式加密：AES
- 關鍵詞：AES, Rijndael
- **sym-aes**（AES（Advanced Encryption Standard））score=16；來源 S01, S04, S06, S12；依據 title/alias:AES; body:AES×3; title/alias:Rijndael; body:Rijndael×3
- **asym-rsa**（RSA：基本運作原理）score=8；來源 S02, S08, S09, S12；依據 title/alias:AES; body:AES×3
- **classical-caesar**（Caesar Cipher（凱撒密碼／位移密碼））score=8；來源 S02, S03；依據 title/alias:AES; body:AES×3
- **mode-gcm-aead**（GCM 與認證加密（Authenticated Encryption, AEAD））score=8；來源 S05, S11；依據 title/alias:AES; body:AES×3

## Slide 19：AES 每一輪的四個步驟
- 關鍵詞：AES, AES-128
- **sym-aes**（AES（Advanced Encryption Standard））score=16；來源 S01, S04, S06, S12；依據 title/alias:AES; body:AES×3; title/alias:AES-128; body:AES-128×3
- **asym-rsa**（RSA：基本運作原理）score=10；來源 S02, S08, S09, S12；依據 title/alias:AES; body:AES×3; body:AES-128×2
- **classical-caesar**（Caesar Cipher（凱撒密碼／位移密碼））score=8；來源 S02, S03；依據 title/alias:AES; body:AES×3
- **mode-gcm-aead**（GCM 與認證加密（Authenticated Encryption, AEAD））score=8；來源 S05, S11；依據 title/alias:AES; body:AES×3
- **app-hybrid-tls**（密碼學在現代網路的應用：混合加密與 HTTPS／TLS 1.3）score=4；來源 S06, S10；依據 body:AES×3; body:AES-128×1

## Slide 20：AES 實例：一步一步看資料怎麼變
- 關鍵詞：AES, AES-128
- **sym-aes**（AES（Advanced Encryption Standard））score=16；來源 S01, S04, S06, S12；依據 title/alias:AES; body:AES×3; title/alias:AES-128; body:AES-128×3
- **asym-rsa**（RSA：基本運作原理）score=10；來源 S02, S08, S09, S12；依據 title/alias:AES; body:AES×3; body:AES-128×2
- **classical-caesar**（Caesar Cipher（凱撒密碼／位移密碼））score=8；來源 S02, S03；依據 title/alias:AES; body:AES×3
- **mode-gcm-aead**（GCM 與認證加密（Authenticated Encryption, AEAD））score=8；來源 S05, S11；依據 title/alias:AES; body:AES×3
- **app-hybrid-tls**（密碼學在現代網路的應用：混合加密與 HTTPS／TLS 1.3）score=4；來源 S06, S10；依據 body:AES×3; body:AES-128×1

## Slide 21：AES 怎麼解密？現在用在哪裡？
- 關鍵詞：AES, AES-GCM
- **mode-gcm-aead**（GCM 與認證加密（Authenticated Encryption, AEAD））score=13；來源 S05, S11；依據 title/alias:AES; body:AES×3; title/alias:AES-GCM
- **asym-rsa**（RSA：基本運作原理）score=8；來源 S02, S08, S09, S12；依據 title/alias:AES; body:AES×3
- **classical-caesar**（Caesar Cipher（凱撒密碼／位移密碼））score=8；來源 S02, S03；依據 title/alias:AES; body:AES×3
- **sym-aes**（AES（Advanced Encryption Standard））score=8；來源 S01, S04, S06, S12；依據 title/alias:AES; body:AES×3
- **app-hybrid-tls**（密碼學在現代網路的應用：混合加密與 HTTPS／TLS 1.3）score=5；來源 S06, S10；依據 body:AES×3; body:AES-GCM×2

## Slide 22：第 4 章：操作模式
- 關鍵詞：AES, AES-128
- **sym-aes**（AES（Advanced Encryption Standard））score=16；來源 S01, S04, S06, S12；依據 title/alias:AES; body:AES×3; title/alias:AES-128; body:AES-128×3
- **asym-rsa**（RSA：基本運作原理）score=10；來源 S02, S08, S09, S12；依據 title/alias:AES; body:AES×3; body:AES-128×2
- **classical-caesar**（Caesar Cipher（凱撒密碼／位移密碼））score=8；來源 S02, S03；依據 title/alias:AES; body:AES×3
- **mode-gcm-aead**（GCM 與認證加密（Authenticated Encryption, AEAD））score=8；來源 S05, S11；依據 title/alias:AES; body:AES×3
- **app-hybrid-tls**（密碼學在現代網路的應用：混合加密與 HTTPS／TLS 1.3）score=4；來源 S06, S10；依據 body:AES×3; body:AES-128×1

## Slide 23：為什麼需要操作模式？先看 ECB 的問題
- 關鍵詞：操作模式, ECB
- **mode-overview**（操作模式（Mode of Operation）：為什麼需要？IV 與填充）score=11；來源 S03, S05；依據 title/alias:操作模式; body:操作模式×3; body:ECB×3
- **mode-ecb**（ECB（Electronic Codebook）模式）score=8；來源 S03, S05；依據 title/alias:ECB; body:ECB×3

## Slide 24：CBC：把區塊一個接一個串起來
- 關鍵詞：CBC, 初始向量
- **mode-overview**（操作模式（Mode of Operation）：為什麼需要？IV 與填充）score=9；來源 S03, S05；依據 body:CBC×3; title/alias:初始向量; body:初始向量×1
- **mode-cbc**（CBC（Cipher Block Chaining）模式）score=8；來源 S01, S03, S05；依據 title/alias:CBC; body:CBC×3

## Slide 25：CTR 與 GCM：現在網路上用的模式
- 關鍵詞：CTR, GCM, 計數器模式
- **mode-ctr**（CTR（Counter）模式）score=16；來源 S05；依據 title/alias:CTR; body:CTR×3; body:GCM×3; title/alias:計數器模式
- **mode-gcm-aead**（GCM 與認證加密（Authenticated Encryption, AEAD））score=11；來源 S05, S11；依據 body:CTR×3; title/alias:GCM; body:GCM×3
- **mode-ecb**（ECB（Electronic Codebook）模式）score=8；來源 S03, S05；依據 title/alias:CTR; body:CTR×3
- **mode-overview**（操作模式（Mode of Operation）：為什麼需要？IV 與填充）score=6；來源 S03, S05；依據 body:CTR×3; body:GCM×3

## Slide 26：第 5 章：公開金鑰加密
- 關鍵詞：金鑰分配問題, GCM, AES-GCM
- **mode-gcm-aead**（GCM 與認證加密（Authenticated Encryption, AEAD））score=13；來源 S05, S11；依據 title/alias:GCM; body:GCM×3; title/alias:AES-GCM
- **sym-concept**（對稱式加密（Symmetric Encryption）與金鑰分配問題）score=7；來源 S02, S06；依據 title/alias:金鑰分配問題; body:金鑰分配問題×2
- **app-hybrid-tls**（密碼學在現代網路的應用：混合加密與 HTTPS／TLS 1.3）score=5；來源 S06, S10；依據 body:GCM×3; body:AES-GCM×2
- **mode-ctr**（CTR（Counter）模式）score=4；來源 S05；依據 body:GCM×3; body:AES-GCM×1

## Slide 27：為什麼需要公開金鑰加密？
- 關鍵詞：公開金鑰, public key, 金鑰分配問題
- **asym-public-key**（公開金鑰密碼學（Asymmetric / Public-Key Cryptography））score=17；來源 S02, S06, S07；依據 title/alias:公開金鑰; body:公開金鑰×3; title/alias:public key; body:public key×3; body:金鑰分配問題×1
- **asym-key-exchange**（Diffie–Hellman 金鑰交換（Key Exchange））score=9；來源 S02, S07, S08, S10；依據 body:公開金鑰×1; title/alias:public key; body:public key×2; body:金鑰分配問題×1
- **sym-concept**（對稱式加密（Symmetric Encryption）與金鑰分配問題）score=8；來源 S02, S06；依據 body:公開金鑰×1; title/alias:金鑰分配問題; body:金鑰分配問題×2

## Slide 28：Diffie–Hellman：在公開場合約定同一把金鑰
- 關鍵詞：Diffie-Hellman, 金鑰交換
- **asym-key-exchange**（Diffie–Hellman 金鑰交換（Key Exchange））score=14；來源 S02, S07, S08, S10；依據 title/alias:Diffie-Hellman; body:Diffie-Hellman×1; title/alias:金鑰交換; body:金鑰交換×3
- **app-hybrid-tls**（密碼學在現代網路的應用：混合加密與 HTTPS／TLS 1.3）score=5；來源 S06, S10；依據 body:Diffie-Hellman×2; body:金鑰交換×3

## Slide 29：RSA（一）：怎麼產生一對金鑰
- 關鍵詞：RSA, RSA modulus
- **asym-rsa**（RSA：基本運作原理）score=14；來源 S02, S08, S09, S12；依據 title/alias:RSA; body:RSA×3; title/alias:RSA modulus; body:RSA modulus×1
- **asym-signature**（數位簽章（Digital Signature））score=8；來源 S02, S06, S08, S09, S10；依據 title/alias:RSA; body:RSA×3

## Slide 30：RSA（二）：加密與解密
- 關鍵詞：RSA, OAEP
- **asym-rsa**（RSA：基本運作原理）score=16；來源 S02, S08, S09, S12；依據 title/alias:RSA; body:RSA×3; title/alias:OAEP; body:OAEP×3
- **asym-signature**（數位簽章（Digital Signature））score=8；來源 S02, S06, S08, S09, S10；依據 title/alias:RSA; body:RSA×3

## Slide 31：數位簽章：私鑰簽、公鑰驗
- 關鍵詞：數位簽章, digital signature
- **asym-signature**（數位簽章（Digital Signature））score=16；來源 S02, S06, S08, S09, S10；依據 title/alias:數位簽章; body:數位簽章×3; title/alias:digital signature; body:digital signature×3

## Slide 32：第 6 章：綜合應用
- 關鍵詞：public key, 數位簽章, AES
- **asym-rsa**（RSA：基本運作原理）score=10；來源 S02, S08, S09, S12；依據 body:public key×1; body:數位簽章×1; title/alias:AES; body:AES×3
- **asym-public-key**（公開金鑰密碼學（Asymmetric / Public-Key Cryptography））score=9；來源 S02, S06, S07；依據 title/alias:public key; body:public key×3; body:數位簽章×1
- **asym-signature**（數位簽章（Digital Signature））score=9；來源 S02, S06, S08, S09, S10；依據 body:public key×1; title/alias:數位簽章; body:數位簽章×3
- **classical-caesar**（Caesar Cipher（凱撒密碼／位移密碼））score=8；來源 S02, S03；依據 title/alias:AES; body:AES×3
- **mode-gcm-aead**（GCM 與認證加密（Authenticated Encryption, AEAD））score=8；來源 S05, S11；依據 title/alias:AES; body:AES×3

## Slide 33：全部組合起來：HTTPS 與 TLS 1.3
- 關鍵詞：TLS 1.3, HTTPS, 憑證
- **app-hybrid-tls**（密碼學在現代網路的應用：混合加密與 HTTPS／TLS 1.3）score=24；來源 S06, S10；依據 title/alias:TLS 1.3; body:TLS 1.3×3; title/alias:HTTPS; body:HTTPS×3; title/alias:憑證; body:憑證×3

## Slide 34：總結：從古典密碼到現代密碼學
- 關鍵詞：AES, 公開金鑰, TLS 1.3, classical cipher weaknesses
- **app-hybrid-tls**（密碼學在現代網路的應用：混合加密與 HTTPS／TLS 1.3）score=11；來源 S06, S10；依據 body:AES×3; title/alias:TLS 1.3; body:TLS 1.3×3
- **mode-gcm-aead**（GCM 與認證加密（Authenticated Encryption, AEAD））score=11；來源 S05, S11；依據 title/alias:AES; body:AES×3; body:TLS 1.3×3
- **asym-rsa**（RSA：基本運作原理）score=10；來源 S02, S08, S09, S12；依據 title/alias:AES; body:AES×3; body:公開金鑰×1; body:TLS 1.3×1
- **sym-aes**（AES（Advanced Encryption Standard））score=9；來源 S01, S04, S06, S12；依據 title/alias:AES; body:AES×3; body:TLS 1.3×1
- **asym-public-key**（公開金鑰密碼學（Asymmetric / Public-Key Cryptography））score=8；來源 S02, S06, S07；依據 title/alias:公開金鑰; body:公開金鑰×3

## Slide 35：參考資料
- 關鍵詞：（不需要）
- 命中：無
