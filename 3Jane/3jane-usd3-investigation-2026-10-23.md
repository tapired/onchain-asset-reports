# 3Jane USD3 / sUSD3: leverage, borrowers and funding links

**Checked October 23, 2026, Istanbul time.** API observations are approximately October 22, 22:19-22:35 UTC. Current balances and historical transaction examples are distinguished below. Amounts are USDC unless a token quantity is specified.

## Bottom line

**There is substantial leveraged demand, and there are direct funding links between major borrowers. But I have not established that 3Jane recycles USD3 backing into the Morpho markets financing that demand.** That missing funding link matters: leveraged minting is proven; an issuer-funded reserve loop is not.

The main flags are:

- **74.17% of outstanding PT-USD3 is pledged in Morpho.** PT issuance is heavily tied to collateralized borrowing, not simply unleveraged fixed-yield investment.
- **The two largest borrowers in the main PT market exchanged USDC directly.** Together they owe **8.56M**, or **44.48%** of that market's debt. This establishes a funding relationship, not common ownership.
- One transaction turned **750k of contributed USDC into 6.715M of USD3-backed positions**, financed with **5.965M of debt**.
- The underlying credit book is concentrated elsewhere: 3Jane reports **62.59M of Slope exposure**, approximately **62.2% of its 100.60M pool TVL**. These are issuer-reported off-chain carrying values, not independently verified cash.

## 1. Who borrows, and who funds the Morpho markets?

These are external collateralized lending markets. They are **not** 3Jane's underlying credit pool, discussed in section 4.

| Market | USDC supplied | USDC borrowed | Largest borrower | Their debt / market share |
|---|---:|---:|---|---:|
| [USD3, 91.5% LLTV](https://app.morpho.org/ethereum/variable/0xe3df58f9d3011b7481ff36b939fa5f8da642f34ea5792d25d3958dbf1efa26d7/usdc-usd3) | 20.60M | 17.93M | [0x0A907...92E8](https://etherscan.io/address/0x0A907C7CE498b6a1d1dC42dAd1acbD97d96392E8) | 5.045M / 28.13% |
| [PT-USD3, `ecabc...`, 86% LLTV](https://app.morpho.org/ethereum/variable/0xecabc12c73a97c766d0c6aeb4c15c635630d78158b2ac8370455a09efcc50837/usdc-pt-usd3-17dec2026) | 7.47M | 6.53M | [0x7A27...e9Bc](https://etherscan.io/address/0x7A27F9586d0895F045b80B3Fb1D9D6eF4D54e9Bc) | 1.726M / 26.43% |
| [PT-USD3, `f8c5...`, 86% LLTV](https://app.morpho.org/ethereum/variable/0xf8c5aa31ea6b2a068a9eddb46dd110cae57bf0f12be9583a3f9a818effecba89/usdc-pt-usd3-17dec2026) | 23.47M | 19.24M | [0x6b28...bE5b](https://etherscan.io/address/0x6b28fb12EE41baA9d1Df16971DE53ADDE6d1bE5b) | 7.276M / 37.82% |

The next-largest USD3 borrower is [0xB47c...5bFD](https://etherscan.io/address/0xB47c72BE8a2968Dec42D3b9d8c6f464224605bFD), owing **2.870M**, plus **820k** in `ecabc...`. The second-largest `f8c5...` borrower is [0x81019...692c](https://etherscan.io/address/0x81019a2B8bbC35bb5B7Cab7e33fD94e4d487692c), owing **1.282M**.

**Main USDC lenders across these three markets:**

| Vault / lender | Combined supply |
|---|---:|
| [3Jane Ecosystem Vault](https://app.morpho.org/ethereum/vault/0xe05faDf242331808f504661BEA65972594869826/3jane-ecosystem-vault), Clearstar | **19.405M** |
| [Yearn OG USDC V1](https://etherscan.io/address/0xF9bdDd4A9b3A45f980e11fDDE96e16364dDBEc49) and [Yearn OG USDC](https://etherscan.io/address/0xBA77D947E23710a397Dd777A47254E1c2bd612C1), combined | **6.959M** |
| [Pendle Ecosystem High Yield USDC, adapter](https://etherscan.io/address/0x0409C3125B86845E77F320200de6945E5995b67e) | **5.237M** |
| [KPK USDC Yield](https://etherscan.io/address/0x4f74895557bEa2dE5d51D8C06E944da92dbC8550) | **3.341M** |
| [Wintermute USDC Select](https://etherscan.io/address/0x3b9e060a2b05588126Fda01b95e9485687Fc91D7) | **2.818M** |
| [Keyrock USDC](https://etherscan.io/address/0x7CA32dCD9269b0BeB21a4F364DED5cfFCB7b3635) | **2.813M** |

The 3Jane Ecosystem Vault supplies **37.65%** of all three markets' USDC and **52.19%** of `f8c5...`. Its market-facing account is adapter [0xB26E...4186](https://etherscan.io/address/0xB26E1c6E89fA002A0751d84C0e99D66657654186). **The vault's name does not prove that its deposits belong to 3Jane or come from USD3 backing.** The largest three vault-share holders are [0xC442...7427](https://etherscan.io/address/0xC44216Cafc0b49E14F9BA40b2c51bed591757427), [0xb459...FF10](https://etherscan.io/address/0xb459c8A41A4ceF0FE752FB8BeF1F7Eea09aCFF10) and [0xaA6A...B3A0](https://etherscan.io/address/0xaA6A99026Af49b583eA5Cb54B883c0bA33E8B3A0); their beneficial owners were not established.

Two additional flags: **7.06M of USD3-market debt has an oracle-based health factor below 1.01**; and the two PT markets use **different oracles**, despite identical collateral and LLTV. Their snapshot prices were approximately **0.96983 versus 0.95474 USDC/PT**. They should not be treated as identical risk markets.

Source: [Morpho API](https://api.morpho.org/graphql), with complete returned borrower/supplier lists and market IDs preserved in the [evidence file](3jane-evidence-2026-10-23.json).

## 2. Confirmed leverage and wallet connections

### 750k equity finances 6.715M of minting

On **September 29, 00:02:59 UTC**, borrower `0x0A907...92E8` executed this in [one transaction](https://etherscan.io/tx/0xb0d4f67fc6a3972925ac7138b6f9189a089f7c0c0e91b4a6082137101d0c9355):

1. Contributed **750,000 USDC** and took a **5,965,324.069027 USDC flash loan**.
2. Deposited **5,530,177.861521 USDC**, receiving **4,686,795.299770 USD3**, then posted that USD3 as collateral.
3. Routed another **1,185,146.207506 USDC** through Pendle into USD3, minting **1,185,146.207505 PT and matching YT**. Posted the PT as collateral and retained the YT.
4. Borrowed **5,017,817.432521 USDC** against USD3 and **947,506.636506 USDC** against PT.
5. Those two debts repaid the flash loan exactly.

**Result: 6.715M of gross mint funding from 750k equity, approximately 8.95x.** This is a leveraged mint financed by borrowing against the newly created claims. The flash loan is not additional debt to count on top. The PT loan entered `f8c5...`; the wallet's current PT position is in `ecabc...`.

The deposits entered the USD3/wrapped-Aave-USDC credit-pool path. This transaction does **not** show that the same reserve funds were subsequently supplied to the external Morpho market.

### The largest two PT borrowers fund each other

For `0x6b28...bE5b`, the September 29 sequence is:

| UTC time | Confirmed action |
|---|---|
| 01:31:23 | [Uses 1,059,368.074598 USD3 to mint 1,250,011.028795 PT and matching YT](https://etherscan.io/tx/0xea6c33252b2f5041cf30d95c1513bce67bb3e8266040741406587b5d3bbc7675). |
| 01:33:11 | [Posts those PT and borrows 350,000 USDC](https://etherscan.io/tx/0xfac2193dd039762356f2dbb9bc31b95482da5a8fa396e80dfb96c5ef3cc491b5). |
| 01:36:23 | [Receives 150,000 USDC from second-largest borrower `0x81019...692c`](https://etherscan.io/tx/0x470fba59b4bad456737845aa2f29d2c027ac621266f9d7faf39705defdb20d34). |
| 02:03:59 | [Sends 250,000 USDC back to that borrower](https://etherscan.io/tx/0x40c68cb0045f164c6243c454c741b45006828602ec4064e39b15e96f8421e369). |

The transfers are successful, direct transfers of genuine USDC, not zero-value/address-poisoning entries. Today the wallets owe **8.558M combined** in `f8c5...`. They each hold YT quantities matching their PT collateral: **9.225M** and **1.623M**, respectively. This supports leveraged PT/YT minting rather than treating their PT collateral as standalone PT purchases.

**Unknown:** why they transferred funds, whether they share an owner, whether either is affiliated with 3Jane, and whether subsequent borrowing was repeatedly reminted.

## 3. Who holds USD3/sUSD3, and who buys PT/YT?

Holding is not necessarily buying: wrappers aggregate users, and minting PT creates matching YT.

| Asset | Largest relevant holders at the snapshot |
|---|---|
| USD3 | Pendle SY **48.48%**; Morpho collateral **20.09%**; sUSD3 contract **8.29%**. Largest non-wrapper wallet: Safe [0x11E1...FD82](https://etherscan.io/address/0x11E1A8540fA9B5F67bDD0AE70761D55fc388FD82), **4.327M USD3 / 5.10%**. |
| sUSD3 | [0xBCB7...98b0](https://etherscan.io/address/0xBCB76036c703eA46710bC7995A71ED00334f98b0), **2.511M sUSD3 / 40.02%**; Pendle SY **34.65%**; [0x17Cd...ca99](https://etherscan.io/address/0x17CdFaA6638A1dEd4dfcde056FC6956EBD19ca99), **4.14%**. |
| PT-USD3 | Morpho holds **34.751M / 74.17%**; Pendle pool **9.47%**. Largest wallet outside those contracts: [0x2b85...D99f](https://etherscan.io/address/0x2b8546F252548371e5459205b48C6475E3EcD99f), **1.047M PT**. |
| YT-USD3 | `0x6b28...bE5b`: **9.225M / 19.69%**; [0xdEB13...0B2F](https://etherscan.io/address/0xdEB13D71998ED256554114cf3c6c150A74C60B2F): **5.908M / 12.61%**; [0x3309...7455](https://etherscan.io/address/0x330998bB5b24452a2f9F11324e2058d9e72B7455): **3.232M / 6.90%**. |
| PT-sUSD3 | Pool **42.94%**; largest wallet [0x09cC...793A](https://etherscan.io/address/0x09cC15Dda77789d42c0133c909E88Fb6E3Af793A): **229,144 PT / 8.62%**. |
| YT-sUSD3 | `0xdEB13...0B2F`: **432,671 / 16.28%**; [0xD01D...22A7](https://etherscan.io/address/0xD01D3969aCd4307e63837D0153fea0213A0322A7): **227,645 / 8.56%**; `0x3309...7455`: **148,734 / 5.59%**. |

**Actual purchases verified, not inferred from holdings:**

- **YT buyer `0xdEB13...0B2F`:** on October 11, [pays 21,771.697939 USD3 for 1,023,627.131173 YT-USD3](https://etherscan.io/tx/0x733de60fe89032e16d7f5ba1d25d56f9211bff6970ed9f1ad3c253fdb21b05a0). The order-fill event identifies the buyer; the transaction sender is not the buyer. This wallet is also the largest YT-sUSD3 holder.
- **PT buyer Safe `0xA1E3...fa89`:** on June 24, [spends 200,000 USDC for 210,611.594144 PT-USD3](https://etherscan.io/tx/0xfa376f6e109358ad32f6a794ec77eb5accf76e0168ef19326031d5b47017a1aa), confirmed by Pendle's swap event. It currently holds **575,806 PT**.

These identities remain unverified. **YT quantities are not dollar values**, and these examples are not an all-time buyer-volume ranking. 3Jane explicitly incentivizes YT and ecosystem lending, providing a plausible reward-farming motive without proving manipulation. [Incentive documentation](https://docs.3jane.xyz/jane/liquidity-mining)

## 4. Who borrows the actual USD3 backing?

The separate [3Jane MorphoCredit contract](https://etherscan.io/address/0xDe6e08ac208088cc62812Ba30608D852c6B0EcBc) has approximately **89.91M USDC-equivalent booked debt** across **14 borrowing addresses**.

- **[0x3Ff3...291b](https://etherscan.io/address/0x3Ff3ff33D20a086834A095ed6ed562c9e189291b): 88.764M / 98.73%.** The official app labels this Safe `EREBOR_STAGING_MULTISIG`. This is the aggregate staging account for the off-chain credit funding path, **not evidence that one retail borrower has 88.8M cash sitting in a wallet**. [Official banking-rail explanation](https://docs.3jane.xyz/backing/fcc/banking-rail-erebor)
- Largest other borrower: [0x6b941...7a7e](https://etherscan.io/address/0x6b9410449200579cf66e641df17d681f71537a7e), **359k**; next [0xbeb69...3c00](https://etherscan.io/address/0xbeb69e7ac7f59bdb79b89fc94ed862c6b39f3c00), **251k**; then [0x541f...e3a1](https://etherscan.io/address/0x541f9ca20d448dc53681077eb54492117b67e3a1), **125k**. Beneficial owners unknown.

The [official backing dashboard](https://app.3jane.xyz/info/backing) reports these facility carrying values:

| Facility | Exposure | Source valuation date |
|---|---:|---|
| Slope, trade-credit forward flow | **62.592M** | October 20 |
| Settle, inventory-financing forward flow | **14.239M** | October 21 |
| LendSwift, consumer-installment warehouse | **6.630M** | October 16 |

These are **reported accounting values including accrued interest**, not independently verified realizable collateral. The dashboard separately reports **2.551M of Erebor staging cash**. The facility table is not an exact reconciliation of the on-chain debt account.

The junior sUSD3 tranche is reported at **8.342M**, about **8.29% of pool TVL**, and absorbs losses before senior USD3. One wallet holds 40% of its token supply. Do not add sUSD3 TVL to USD3 TVL as separate backing: sUSD3 holds USD3. [Tranche structure](https://docs.3jane.xyz/usd3-susd3/suppliers)

## Assessment and limits

**What is established:** leveraged minting, high PT collateral concentration, a funding connection between the largest two PT borrowers, concentrated ecosystem lending, and concentrated issuer-reported off-chain credit exposure.

**What is not established:** issuer-owned borrower wallets, wash trading, or a closed path from USD3 backing into the USDC loans used to mint more USD3. That requires tracing the Ecosystem Vault's depositors and proving the origin of their funds, not relying on its branding.

This is a public-data investigation, not a complete source-of-funds audit. Holder snapshots cover the top addresses, not all underlying beneficiaries. Balances come from separate API observations; core debt uses stored borrow accounting at Ethereum block **26,251,134**, converted from wrapped Aave USDC, rather than a new interest-accrual simulation. Historical transactions prove those particular actions, not every later use of proceeds. Full Morpho position lists, holder snapshots, decoded transaction evidence and reported facility data are preserved in [the accompanying JSON](3jane-evidence-2026-10-23.json).
