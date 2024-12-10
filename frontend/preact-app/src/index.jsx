import { useState, useEffect } from "preact/hooks";
import { createUser } from "./services/userService";

const App = () => {
  const [users, setUsers] = useState([]);

  const addUser = async () => {
    const newUser = { name: "Saeed :3", email: "saeedsaeed@example.com" };
    const response = await createUser(newUser);
    console.log(response);
  };

  return (
    <div>
      <button onClick={addUser}>Add User</button>
    </div>
  );
};

export default App;
