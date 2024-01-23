<div class="bigcard">   
    <div class="title">
        <h4>Keystroke Verification</h4>
    </div> 
</div> 
<div class="container">

<div class="bigcard">   
    <div class="container">
      <h2><b>Claim Id</b></h2>
    </div>
    <div class="tab1cards">
        {#each Object.values(users) as d}
        <div class="bigcard-user">   
        <div class="container profile" role="button" on:click={() => navigate(d.id)}>
          <!-- Make this clickable -->
          <img class="avatar" src="https://www.w3schools.com/howto/img_avatar.png" alt="users" />
          <div class="container">
            <h4><b>{d.name}</b></h4>
          </div>
        </div>
        </div>
        {/each}
      </div>

    </div>
    <div class="container">
      <p>or else</p>
      <h3><button class="button" on:click={() => goto("/registration")}>Click to register</button></h3>
    </div>
  </div>
  
  <script>
    import { goto } from '$app/navigation';
    import { onMount } from 'svelte';
  
    let users = [];
  
    onMount(async () => {
      await loadUsers();
    });
  
    // Function that returns the users
    async function loadUsers() {
      const response = await fetch(`http://localhost:3000/users/`); // URL to your API
      users = await response.json();
      console.log(users);
    }
  
    // Function that handles navigation through pages
    function navigate(id) {
      $claim = true;
      $userid = id;
      console.log($userid);
      goto("/insert-phrases");
    }
  
    // Importing the store variables
    import { claim, userid } from '../stores/store.js';
  </script>
  