import React from "react";
import Todo from "./todo";

interface Props {
  todos: Todo[];
  toggleTodos: (checked: boolean) => void;
}

const TodoToggle: React.FC<Props> = props => {
  const toggleAll = (event: React.ChangeEvent<HTMLInputElement>) => {
    const checked = event.target.checked;
    props.toggleTodos(!checked);
  };

  const activeTodos = props.todos.reduce(
    (acc, todo) => acc + (todo.active ? 1 : 0),
    0
  );

  return (
    <>
      <input
        id="toggle-all"
        className="toggle-all"
        type="checkbox"
        onChange={toggleAll}
        checked={activeTodos === 0}
      />
      <label htmlFor="toggle-all">Mark all as complete</label>
    </>
  );
};

export default TodoToggle;
