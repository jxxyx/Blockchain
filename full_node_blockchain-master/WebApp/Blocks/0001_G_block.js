let blockchain = document.querySelector("blockchain");

let blockID;
let name;
// Function call for creating Genesis block

createBlock(2);
function createBlock(
  blockID,
  transactionId,
  name = "Norbert BM",
  href = "https://github.com/NorbertBM"
) {
  let newChain = ` 
  <i class="fas fa-link"></i>
  `;
  let chain = document.createElement("chain-link");

  chain.innerHTML = newChain;

  let newBlock = `

  <div class="card-header">
    <span class="display-4">Block ${blockID} </span>
    <p>
    <a href="${href}" target=_blank class="text-info">(${name})</a>
    </p>
  </div>

  <ul class="list-group list-group-flush">
    <li class="list-group-item">
      <h5>Block ID</h5>
      <span class="text-muted">${blockID}</span>
      <h5>Transaction ID</h5>
      <span class="text-muted">${transactionId}</span>
    </li>

    <li class="list-group-item">
      <h5>Hash</h5>
      <span class="hash"
        >${generateHash()}</span
      >
      <h5>Hash of previous block</h5>
      <span class="text-muted"
        >${getPrevHash()}</span
      >
    </li>

    <li class="list-group-item">
      <h6>Nonce</h6>
      <span class="text-muted">0</span>
    </li>
    <li class="list-group-item">
      <h6>Timestamp</h6>
      <span class="text-muted">${blockTimestamp()}</span>
    </li>
  </ul>

    `;
  let block = document.createElement("block");
  block.className = "card block";
  block.innerHTML = newBlock;
  //todo: Add new block to the blockchain
  blockchain.append(block);

  //todo: Add new chain to the blockchain
  blockchain.append(chain);
  // blockchain.prepend(chain);
}

// Function to generate a new random Hash

function generateHash() {
  let result = "";
  const characters =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  const charactersLength = characters.length;
  for (let i = 0; i < 256; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}
// Function to get previous Hash

function getPrevHash() {
  let blocks = blockchain.querySelectorAll(".block");

  if (blocks.length > 1) {
    let secondLastBlock = blocks[blocks.length - 2];
    let prevHash = secondLastBlock.querySelector(".hash").innerText;
    return prevHash;
  } else {
    return null;
  }
}

function blockTimestamp() {
  const currentDate = new Date();

  const currentDayOfMonth = currentDate.getDate();
  // Add 1 because getMonth() returns 0-11
  const currentMonth = currentDate.getMonth() + 1; 
  const currentYear = currentDate.getFullYear();
  // Get hours, minutes, and seconds
  const hours = currentDate.getHours();
  const minutes = currentDate.getMinutes();
  const seconds = currentDate.getSeconds();

  // Pad single digits with leading zero
  const dayStr = currentDayOfMonth.toString().padStart(2, '0');
  const monthStr = currentMonth.toString().padStart(2, '0');
  const hoursStr = hours.toString().padStart(2, '0');
  const minutesStr = minutes.toString().padStart(2, '0');
  const secondsStr = seconds.toString().padStart(2, '0');

  // Format the date and time as 'DD-MM-YYYY HH:MM:SS'
  return `${dayStr}-${monthStr}-${currentYear} ${hoursStr}:${minutesStr}:${secondsStr}`;
}

console.log(blockTimestamp());
