import React from "react";
import Todo from "./todo";
import TodoItem from "./TodoItem";

interface Props {
  todos: Todo[];
  saveTodo: (todo: Todo, text: string) => void;
  toggleTodo: (todo: Todo, active: boolean) => void;
  removeTodo: (todo: Todo) => void;
}

const List: React.FC<Props> = props => {
  return (
    <ul className="todo-list">
      {props.todos.map(todo => (
        <TodoItem
          key={todo.id}
          todo={todo}
          saveTodo={props.saveTodo.bind(null, todo)}
          toggleTodo={props.toggleTodo.bind(null, todo)}
          removeTodo={props.removeTodo.bind(null, todo)}
        />
      ))}
    </ul>
  );
};

export default List;
