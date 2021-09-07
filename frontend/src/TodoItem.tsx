import React from "react";
import Todo from "./todo";

interface Props {
  todo: Todo;
  saveTodo: (text: string) => void;
  toggleTodo: (active: boolean) => void;
  removeTodo: () => void;
}

const TodoItem: React.FC<Props> = props => {
  const inputElement = React.useRef<HTMLInputElement>(null);
  const [editText, setEditText] = React.useState(props.todo.text);
  const [editing, setEditing] = React.useState(false);

  React.useEffect(() => {
    if (editing) {
      const current = inputElement.current;
      if (current) {
        current.focus();
      }
    }
  }, [editing]);

  const { todo } = props;

  const classes = [
    todo.active ? "" : "completed",
    editing ? "editing" : ""
  ].join(" ");

  const onDoubleClick = () => {
    setEditing(() => true);
  };

  const handleSubmit = (event?: React.FocusEvent<HTMLInputElement>) => {
    const value = editText.trim();
    if (value) {
      props.saveTodo(value);
    } else {
      props.removeTodo();
    }
    setEditing(() => false);
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Escape") {
      setEditText(() => props.todo.text);
      setEditing(() => false);
    } else if (event.key === "Enter") {
      handleSubmit();
    }
  };

  return (
    <li className={classes}>
      <div className="view">
        <input
          className="toggle"
          type="checkbox"
          checked={!todo.active}
          onChange={e => props.toggleTodo(!todo.active)}
        />
        <label onDoubleClick={onDoubleClick}>{todo.text}</label>
        <button className="destroy" onClick={props.removeTodo} />
      </div>
      <input
        ref={inputElement}
        className="edit"
        value={editText}
        onChange={e => setEditText(e.target.value)}
        onBlur={handleSubmit}
        onKeyDown={handleKeyDown}
      />
    </li>
  );
};

export default TodoItem;
