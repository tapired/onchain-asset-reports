Reservoir: Confirmed Borrow-and-Remint Loop

**Date:** September 21, 2026. All times below are UTC.  
**Chain / protocol:** Ethereum / Dolomite.  
**Borrower:** [0x086eb9C2B14dD657ae77D07dF9115A2F946CE327](https://eth.blockscout.com/address/0x086eb9C2B14dD657ae77D07dF9115A2F946CE327).

## Loop Size

**11 verified rounds totaling 14,545,000 USD1 (approximately $14.545M) borrowed and used to mint new rUSD/wsrUSD.**

Each round follows the same order: **borrow USD1 from Dolomite -> mint rUSD and convert to wsrUSD -> deposit the newly minted wsrUSD into the same Dolomite borrowing account -> repeat.**

This is cumulative borrowed-and-reminted volume for this sequence, not fresh investor capital, the borrower's total debt, or total protocol-wide circular exposure.

## Transactions in Order

Each timestamp links to its transaction. Read each row from left to right, then continue to the next row. The amount is the USD1 borrowed and used for minting, not the number of wsrUSD shares.

| Round | USD1 borrowed and reminted | 1. Borrow | 2. Mint rUSD / wsrUSD | 3. Deposit wsrUSD collateral |
|---|---:|---|---|---|
| 1 | 2,450,000 | [18:34:11](https://eth.blockscout.com/tx/0x5bd79360127511da82d8187a85e425e3d5ca1d7ef114e6fa68799c3f433ce72d) | [18:37:59](https://eth.blockscout.com/tx/0x67bc7db4fb318900619f4d3216ea44e8792de87b1418bd3b213eb4ca47d433d5) | [18:39:59](https://eth.blockscout.com/tx/0xc658606acb83b876cda6549676fb2501be9ec1350c19132c966e7cc59e8cce50) |
| 2 | 2,125,000 | [18:42:23](https://eth.blockscout.com/tx/0x803e0a7a6a47f0a0247bc8bd6539a038b4dd9ea8b7235c33e5deb764358e4665) | [18:45:11](https://eth.blockscout.com/tx/0x76ad09fde861df21379109ca7c406e58ad68e0933892771ad9a347587b44ac16) | [18:46:47](https://eth.blockscout.com/tx/0x6b3d237c7a78ee8410806ce62f8bcacea9f75bcf44b9d36b752cf22df82e4526) |
| 3 | 1,850,000 | [18:49:23](https://eth.blockscout.com/tx/0x692f20231928791216d57cc0fe98051873e3ebf4f0f117a3a8f058e07a518a10) | [18:52:47](https://eth.blockscout.com/tx/0xcfcab29a8049c6e8e41e6911ff38fb8c38ab714922982a48124d0ecefe5859c6) | [18:58:59](https://eth.blockscout.com/tx/0xdf4ca5b8cb2ce276fd0bad0ef92dab410be05b050145c477b1524cf7a5ff7a7b) |
| 4 | 1,600,000 | [19:02:11](https://eth.blockscout.com/tx/0xb6a9bda27467f5b1e46b079a9c5ec490ced294587c956540db8f480305ccb55e) | [19:04:47](https://eth.blockscout.com/tx/0x92945380a230edbddd23291f8628f368e2da570f374affbfa9422fff8627e350) | [19:05:47](https://eth.blockscout.com/tx/0xb23ab54c1a97e7e3ef26511001d63e546cf4557c60b8a8b028501d6abd9b16c3) |
| 5 | 1,380,000 | [19:08:11](https://eth.blockscout.com/tx/0x98c952fd4a81e96b3bd2a5dac4e1c90acc83d245c4e2c9442a2b3008d50bd25a) | [19:10:59](https://eth.blockscout.com/tx/0xb6bbb887961e2214509e3ec8da0ab0305b05aa22c0e1ae45706f23208e26a2bf) | [19:16:47](https://eth.blockscout.com/tx/0x5773e8df81bc494c1b914905b5597a443ff2542fa5518bedb8f9ffaf3d1ec470) |
| 6 | 1,200,000 | [19:19:11](https://eth.blockscout.com/tx/0xb0b8f865af6fbd532c1e30dbe7b628339f2cd4bf889e5d67785a153d809c3080) | [19:22:47](https://eth.blockscout.com/tx/0x58383147693c64d8a4ef616dde5164c8aa3e9aa0bc6b743c43e1795356719848) | [19:24:23](https://eth.blockscout.com/tx/0x71eb16a7578665a8c1f11c91e7b89b99d376fe9a89a287e1371167b758e81b25) |
| 7 | 1,030,000 | [19:28:11](https://eth.blockscout.com/tx/0x6acf062abf69df88ad8b0542cbf724780c766ebe6208de4d8491ebd420c8eef4) | [19:30:59](https://eth.blockscout.com/tx/0x7a3273af22c57bc9f19f4786a1029a0c1d4bdd02b206139632ae4376374fcaec) | [19:32:35](https://eth.blockscout.com/tx/0x6ae02ce27ac5b088e43efdcfc49c1d8924947c889000e176bcb28098f5d3d7a4) |
| 8 | 900,000 | [19:34:47](https://eth.blockscout.com/tx/0xa020aae1d0a5637369e55e114a61b63c950d25af890a418b1fc95dcf9176e715) | [19:36:47](https://eth.blockscout.com/tx/0xed9faf6eb7e4ee38802a0ffc6ad691edef823b179b0a132fa0bdd6726df79aaa) | [19:37:59](https://eth.blockscout.com/tx/0x95ac54cc5ee2c0d14aa0e8c31f6cea545bc2330d6f9e82b1f388845c36d8fb30) |
| 9 | 775,000 | [19:39:35](https://eth.blockscout.com/tx/0xc8439c8d136746b929c5839bbf147dc6925df1ccfdd1acee587539d895ee4b1c) | [19:41:47](https://eth.blockscout.com/tx/0x7571406bca7cc1c048035e7837816c01e8f04470dcd55f29dd6e778fa1f52b09) | [19:42:59](https://eth.blockscout.com/tx/0x7a461bea16bdc213656c7925f2c78812bc349f710222527a2eee8e77e7a4f712) |
| 10 | 650,000 | [19:44:47](https://eth.blockscout.com/tx/0xa1397a1a3723171e2b32ce62dea9b04c22f12bc8efe551870e5e9b5552f4c313) | [19:47:23](https://eth.blockscout.com/tx/0xcc6894044736a4f8b3eeb11316dadb555a463e72220b79302dec4cb43d3dbecd) | [19:49:59](https://eth.blockscout.com/tx/0x323fd07c17d6da35dfab270d7b4bc9f550442811e4054194cf8ebcc0b4e832e2) |
| 11 | 585,000 | [19:52:35](https://eth.blockscout.com/tx/0xd8015049ba1d8a905fc86077aa1fb0accf734b822283f39575ff268744ab1ccb) | [19:56:59](https://eth.blockscout.com/tx/0x91049d1523cf62665aaddefff3dd2caf1b99df0641be32ad94f997accad2fb24) | [19:58:47](https://eth.blockscout.com/tx/0x4644d357d0bdadc2d40010dba7790adeace5a5f9a42c8ab64c4d383235c288f7) |
| **Total** | **14,545,000** | | | |

Dolomite's withdrawal events show negative debt balances increasing; these were borrowings, not withdrawals of existing deposits. The new wsrUSD was deposited into the same account that borrowed the USD1.

## Reserve Funds Returned to Dolomite

After the 11 rounds, Reservoir moved the same aggregate amount back into Dolomite:

| Time UTC | Action | Transaction |
|---|---|---|
| 20:39:11 | Reservoir's Safe withdrew **14,545,000 USD1** from its USD1 PSM and transferred it to reserve wallet `0x289C204B35859bFb924B9C0759A4FE80f610671c`. | [PSM withdrawal / reserve transfer](https://eth.blockscout.com/tx/0x7a4c99cc2498c718938ff732911a638b61d0917a39bbcf1b08f41e89b9992410) |
| 20:40:23 | The reserve wallet supplied **14,545,000 USD1** to Dolomite's USD1 market. | [Dolomite supply](https://eth.blockscout.com/tx/0xe91d7ac02c088e3bc55a384a8f75a067d3e057139d7baa898ce0a72d6450c09d) |

**Documented circle:** Dolomite USD1 -> borrower -> Reservoir mint -> wsrUSD collateral -> more borrowing; Reservoir mint proceeds -> reserve wallet -> Dolomite USD1 supply.

This confirms the loop for this borrower and sequence. It does not establish that Reservoir owns the borrower or that every dollar in Dolomite came from Reservoir.

