<script lang="ts">

  // TODO:
  //   - Validate User Input
  //   - Clear User Input When Successful
  //   - Store User Input When Typed
  //   - Add LLM Logic to Get Order Items From User Input
  //   - Use LLM Response to Update Item Counts and Render the Order

  interface Order {
    id: number;
    items: { item: Item, quantity: number }[];
    valid: boolean;
  }

  interface Item {
    // id: number;
    name: string;
  }

  let burgers = 0;
  let fries = 0;
  let drinks = 0;
  let orders: Order[] = [];
  let loading = false;
  let userInput = "";
  let result = "";

  async function placeOrder() {
    loading = true;
    try {
      const response = await fetch(`${import.meta.env.FAST_API_BACKEND_URL}/place-order`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({order: userInput})
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }
      const data = await response.json();
      result = data.placed_order;
      userInput = "";
    } catch (error) {
      console.error(error);
      result = "Something went wrong.";
    } finally {
      loading = false;
    }
    // use a temporary public API for testing
    // const res = await fetch("https://jsonplaceholder.typicode.com/users");
    // orders = await res.json();
    orders = [
      {id: 1, items: [{item: {name: "Burger"}, quantity: 2}, {item: {name: "Fries"}, quantity: 2}], valid: true},
      {id: 2, items: [{item: {name: "Burger"}, quantity: 1}, {item: {name: "Fries"}, quantity: 2}, {item: {name: "Drink"}, quantity: 1}], valid: true},
      {id: 3, items: [{item: {name: "Drink"}, quantity: 4}], valid: false},
    ];
    console.log(userInput)
  }
</script>
<div class="flex m-10 justify-evenly">
  <div class="bg-blue-500 text-white p-5 rounded-lg shadow-md">Total # of Burgers: {burgers}</div>
  <div class="bg-blue-500 text-white p-5 rounded-lg shadow-md">Total # of Fries: {fries}</div>
  <div class="bg-blue-500 text-white p-5 rounded-lg shadow-md">Total # of Drinks: {drinks}</div>
</div>

<div class="flex m-10 mt-[100px] justify-center">
  <input
    type="text"
    placeholder="What Would You Like To Order?"
    class="outline rounded-md p-3 m-9 w-1/3 text-lg"
    bind:value={userInput}
  >
  <button on:click={placeOrder} class="outline rounded-md p-3 m-10 bg-green-500">
    Place Order
  </button>
</div>

<div class="flex justify-center">
  <div class="w-3/4 justify-center">
    {#if loading}
      <p>Loading...</p>
    {:else if orders.length}
    <ul class="block ml-20 mr-20">
      <h3>Order History:</h3>
        {#each orders as order}
      <li class="flex justify-between p-3 m-3 rounded-lg outline {!order.valid && "line-through"}"><span>Order #{order.id}</span><span>{order.items.map((item) => {
        return (
          ` ${item.quantity} ${item.item.name}`
        )
      })}</span></li>
        {/each}
      </ul>
    {/if}
  </div>
</div>
