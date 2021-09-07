import React from "react";
import Todo from "./todo";

interface Props {
  todos: Todo[];
}

const List: React.FC<Props> = props => {
  const activeTodos = props.todos.filter(todo => todo.active).length;
  return (
    <footer className="footer">
      <span className="todo-count">
        {activeTodos} {activeTodos === 1 ? " item" : " items"} left
      </span>
    </footer>
  );
};

export default List;
