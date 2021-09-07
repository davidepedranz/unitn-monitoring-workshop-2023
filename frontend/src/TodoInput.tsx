import React from "react";

interface HeaderProps {
  addTodo: (text: string) => void;
}

const TodoInput: React.FC<HeaderProps> = props => {
  const handleNewTodoKeyDown = (
    event: React.KeyboardEvent<HTMLInputElement>
  ) => {
    if (event.key !== "Enter") {
      return;
    }
    event.preventDefault();

    const inputField = event.currentTarget;
    const value = inputField.value;
    if (value.trim().length > 0) {
      props.addTodo(inputField.value);
      inputField.value = "";
    }
  };

  return (
    <input
      className="new-todo"
      placeholder="What needs to be done?"
      onKeyDown={handleNewTodoKeyDown}
      autoFocus={true}
    />
  );
};

export default TodoInput;
