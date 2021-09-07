import React from "react";
import Todo from "./todo";
import TodoInput from "./TodoInput";
import TodoList from "./TodoList";
import TodoFooter from "./TodoFooter";
import TodoToggle from "./TodoToggle";
import * as apis from "./apis";
import "todomvc-app-css/index.css";

const TodoApp: React.FC = () => {
  const [todos, setTodos] = React.useState([] as Todo[]);

  React.useEffect(() => {
    apis.loadTodos().then(
      todos => {
        setTodos(_ => todos);
      },
      error => {
        // ignore this error on purpose
      }
    );
  }, []);

  const createTodo = (text: string) => {
    apis.createTodo(text).then(
      result => {
        const todo: Todo = { id: result.id, text: text, active: true };
        setTodos(todos => [...todos, todo]);
      },
      error => {
        // ignore this error on purpose
      }
    );
  };

  const updateTodo = (todo: Todo, text: string) => {
    apis.updateTodo(todo.id, text).then(
      _ => {
        setTodos(todos =>
          todos.map(current => ({
            ...current,
            text: current === todo ? text : current.text
          }))
        );
      },
      error => {
        // ignore this error on purpose
      }
    );
  };

  const toggleTodo = (todo: Todo, active: boolean) => {
    const action = active ? apis.activateTodo : apis.deactivateTodo;
    action(todo.id).then(
      _ => {
        setTodos(todos =>
          todos.map(current => ({
            ...current,
            active: current === todo ? active : current.active
          }))
        );
      },
      error => {
        // ignore this error on purpose
      }
    );
  };

  const removeTodo = (todo: Todo) => {
    apis.deleteTodo(todo.id).then(
      _ => {
        setTodos(todos => todos.filter(current => current !== todo));
      },
      error => {
        // ignore this error on purpose
      }
    );
  };

  const toggleTodos = (active: boolean) => {
    const action = active ? apis.activateTodo : apis.deactivateTodo;
    Promise.all(todos.map(todo => action(todo.id))).then(
      _ => {
        setTodos(todos => todos.map(todo => ({ ...todo, active: active })));
      },
      error => {
        // ignore this error on purpose
      }
    );
  };

  return (
    <section className="todoapp">
      <header className="header">
        <h1>todos</h1>
        <TodoInput addTodo={createTodo} />
      </header>
      <section className="main">
        {todos.length > 0 ? (
          <TodoToggle todos={todos} toggleTodos={toggleTodos} />
        ) : null}
        <TodoList
          todos={todos}
          saveTodo={updateTodo}
          toggleTodo={toggleTodo}
          removeTodo={removeTodo}
        />
      </section>
      {todos.length > 0 ? <TodoFooter todos={todos} /> : null}
    </section>
  );
};

export default TodoApp;
