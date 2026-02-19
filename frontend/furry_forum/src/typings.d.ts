export interface Post {
    id: number;
    title: string;
    content: string;
    category: "books" | "discussions" | "news" | "posts";
    imageUrl?: string;
}

export type PostsResponse = Post[]; 