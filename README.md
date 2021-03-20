# lamden-timelock
Smart Contract to lock tokens on Lamden

`con_timelock.py` - The smart contract itself  
`approve.py` - Approve the smart contract to spend your TAU. Needed to be able to lock TAU  
`frontend.py` - Web interface to lock and unlock  

### How to use
1. Approve contract to spend your TAU (or any other token) with `approve.py`. You need to set the privkey in there
2. Run `frontend.py`. To lock tokens: http://0.0.0.0:8000/lock and enter needed data (contract is `currency` if you want to lock TAU)
3. It will return a tx hash. Check that hash in the explorer https://testnet.lamden.io and extract the `result`
4. After locktime is over: http://0.0.0.0:8000/unlock and enter the value you copied from `result`

Thanks to MarViN for providing the code to be able to lock any token and not just TAU. Thanks man!
