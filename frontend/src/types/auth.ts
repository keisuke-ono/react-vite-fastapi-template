export interface User {
  id: string;
  email: string;
  username: string;
  is_active: boolean;
  created_at: string;
  updated_at: string | null;
  last_login: string | null;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface LoginResponse {
  token: Token;
  user: User;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthState {
  user: User | null;
  token: Token | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
} 