
<div class="title"><h4>Keystroke Identification</h4></div>
<div class="bigcard">
  <div class=container>
    <h2><b>Claim Id</b></h2>
  </div>
  <div class="tab1cards">
    <div class="container profile">
      <img class="avatar" src="https://www.w3schools.com/howto/img_avatar.png" alt="users">
      <div class=container>
        <h4><b>Nunzia</b></h4>
      </div>
    </div>
    <div class="container profile">
      <img class="avatar" src="https://www.w3schools.com/howto/img_avatar.png" alt="users">
      <div class=container>
        <h4><b>Elena</b></h4>
      </div>
    </div>
    
    <div class="container profile">
      <img class="avatar" src="https://www.w3schools.com/howto/img_avatar.png" alt="users">
      <div class=container>
        <h4><b>Tommaso</b></h4>
      </div>
    </div>
    <div class="container profile">
      <img class="avatar" src="https://www.w3schools.com/howto/img_avatar.png" alt="users">
      <div class=container>
        <h4><b>Mary</b></h4>
      </div>
    </div>
  </div>    
  <div class="container">
    <p>or else</p>
    <h3><button class="button" on:click={()=>goto("/registration")}>Click to register</button></h3>
  </div>
</div>



<script>
  //function that returns the users - connect to db
  //function that after click on user, navigate to insert-phrases like below
    //find a way to know if you go to insert-phrases through enrollment or through identification
  let visible = true;

  function toggleVisible() {
    visible = !visible
  }

  import {goto} from '$app/navigation';

</script>