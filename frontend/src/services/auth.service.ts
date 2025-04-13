import axios from 'axios';
import { LoginCredentials, LoginResponse, User } from '@/types/auth';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class AuthService {
  private static instance: AuthService;
  private token: string | null = null;

  private constructor() {
    this.token = localStorage.getItem('token');
  }

  public static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService();
    }
    return AuthService.instance;
  }

  public async login(credentials: LoginCredentials): Promise<LoginResponse> {
    try {
      const response = await axios.post<LoginResponse>(
        `${API_URL}/api/v1/login`,
        credentials
      );
      this.setToken(response.data.token.access_token);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.detail || 'Login failed');
      }
      throw error;
    }
  }

  public async getCurrentUser(): Promise<User> {
    try {
      const response = await axios.get<User>(`${API_URL}/api/v1/me`, {
        headers: this.getAuthHeader()
      });
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(error.response?.data?.detail || 'Failed to get user info');
      }
      throw error;
    }
  }

  public logout(): void {
    localStorage.removeItem('token');
    this.token = null;
  }

  public getToken(): string | null {
    return this.token;
  }

  private setToken(token: string): void {
    this.token = token;
    localStorage.setItem('token', token);
  }

  public getAuthHeader(): { Authorization: string } | {} {
    return this.token ? { Authorization: `Bearer ${this.token}` } : {};
  }
}

export const authService = AuthService.getInstance(); 