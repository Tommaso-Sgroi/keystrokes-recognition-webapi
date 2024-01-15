
<div class="title"><h4>Keystroke Verification</h4></div>
<div class="bigcard">
  <div class=container>
    <h2><b>Claim Id</b></h2>
  </div>
  <div class="tab1cards">
  {#each Object.values(users) as d}
     <div class="container profile" role="" on:click={navigate(d.id)}> <!--make this clickable-->
      <img class="avatar" src="https://www.w3schools.com/howto/img_avatar.png" alt="users">
      <div class=container>
        <h4><b>{d.name}</b></h4>
      </div>
    </div>
  {/each}
  </div>    
  <div class="container">
    <p>or else</p>
    <h3><button class="button" on:click={() => goto("/registration")}>Click to register</button></h3>
  </div>
</div>

<script>
  
  import {goto} from '$app/navigation';
  import { onMount } from 'svelte';
  onMount(async ()=> {
    await loadUsers();
  })
  let users=[]

  //function that returns the users
  async function loadUsers() {
    const response = await fetch(`http://localhost:3000/users/`); //url api
    users = await response.json();
    console.log(users)
    return { users };
  } 
  
  //function that handles navigation through pages
  function navigate(id){
    $claim = true
    $userid = id;
    console.log($userid)
    goto("/insert-phrases")
  }
  import { claim, userid } from '../stores/store.js';

</script>