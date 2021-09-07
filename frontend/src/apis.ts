const baseUrl = process.env.REACT_APP_API_BASE_URL || "http://localhost:5000";

export const loadTodos = async () => {
  const res = await fetch(`${baseUrl}/todos/`);
  return await res.json();
};

export const createTodo = async (text: string) => {
  const res = await fetch(`${baseUrl}/todos/`, {
    method: "POST",
    body: JSON.stringify({ text: text }),
    headers: { "Content-Type": "application/json" }
  });
  return await res.json();
};

export const updateTodo = async (id: string, text: string) => {
  return await fetch(`${baseUrl}/todos/${id}`, {
    method: "PATCH",
    body: JSON.stringify({ text: text }),
    headers: { "Content-Type": "application/json" }
  });
};

export const activateTodo = async (id: string) => {
  return await fetch(`${baseUrl}/todos/${id}/activate`, { method: "POST" });
};

export const deactivateTodo = async (id: string) => {
  return await fetch(`${baseUrl}/todos/${id}/deactivate`, { method: "POST" });
};

export const deleteTodo = async (id: string) => {
  return await fetch(`${baseUrl}/todos/${id}`, { method: "DELETE" });
};
