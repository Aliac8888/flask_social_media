import { apiUrl } from "./backend.js";

export type Post = {
  content: string;
  author: string;
  creation_time?: string;
  _id: string;
};

export async function getPosts(): Promise<Post[]> {
  const response = await fetch(new URL("posts/", apiUrl));
  const data = await response.json();
  return data.posts.map((post: any) => ({
    ...post,
    date: new Date(post.creation_time), // Convert string to Date object.
  }));
}

export async function createPost(postData: Partial<Post>) {
  const response = await fetch(new URL("posts/", apiUrl), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      content: postData.content,
      author: "6761f019eff4f614566204e3",
    }),
  });

  return response.json();
}

export async function updatePost(postId: string, patchData: Partial<Post>) {
  const response = await fetch(new URL(`posts/${postId}`, apiUrl), {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(patchData),
  });

  return response;
}