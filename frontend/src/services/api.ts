/**
 * Serviço principal de API para comunicação com o backend
 * ARBOSOCIAL - Sistema Integrado de Análise e Predição de Arboviroses
 */

import axios, { AxiosInstance, AxiosResponse } from 'axios';

// Configuração base da API
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Interfaces TypeScript
export interface User {
  id: number;
  email: string;
  name: string;
  institution?: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

export interface Municipality {
  id: number;
  ibge_code: string;
  name: string;
  state: string;
  region: string;
  population?: number;
  area_km2?: number;
}

export interface ArbovirusCase {
  id: number;
  municipality_id: number;
  disease: 'dengue' | 'zika' | 'chikungunya';
  epidemiological_week: number;
  year: number;
  confirmed_cases: number;
  probable_cases: number;
  deaths: number;
  incidence_rate?: number;
  notification_date?: string;
}

export interface SocialIndicator {
  id: number;
  municipality_id: number;
  year: number;
  population_density?: number;
  urban_population_pct?: number;
  gdp_per_capita?: number;
  gini_index?: number;
  poverty_rate?: number;
  unemployment_rate?: number;
  literacy_rate?: number;
  education_index?: number;
  infant_mortality_rate?: number;
  life_expectancy?: number;
  health_coverage_pct?: number;
  water_supply_pct?: number;
  sewage_treatment_pct?: number;
  garbage_collection_pct?: number;
  electricity_access_pct?: number;
}

export interface Prediction {
  id: number;
  municipality_id: number;
  disease: string;
  model_name: string;
  prediction_date: string;
  target_week: number;
  target_year: number;
  predicted_cases: number;
  confidence_interval_lower?: number;
  confidence_interval_upper?: number;
  model_accuracy?: number;
}

export interface Alert {
  id: number;
  municipality_id: number;
  disease: string;
  alert_level: 'low' | 'medium' | 'high' | 'critical';
  alert_type: string;
  message?: string;
  predicted_cases?: number;
  confidence_score?: number;
  is_active: boolean;
  created_at: string;
  resolved_at?: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  user: User;
}

// Classe principal do serviço de API
class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Interceptor para adicionar token de autenticação
    this.api.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Interceptor para tratar respostas e erros
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Token expirado ou inválido
          localStorage.removeItem('access_token');
          localStorage.removeItem('user');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Métodos de autenticação
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response: AxiosResponse<AuthResponse> = await this.api.post('/auth/login', credentials);
    return response.data;
  }

  async logout(): Promise<void> {
    await this.api.post('/auth/logout');
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  }

  async getCurrentUser(): Promise<User> {
    const response: AxiosResponse<User> = await this.api.get('/auth/me');
    return response.data;
  }

  // Métodos para municípios
  async getMunicipalities(params?: {
    state?: string;
    region?: string;
    search?: string;
  }): Promise<Municipality[]> {
    const response: AxiosResponse<Municipality[]> = await this.api.get('/data/municipalities', { params });
    return response.data;
  }

  async getMunicipality(id: number): Promise<Municipality> {
    const response: AxiosResponse<Municipality> = await this.api.get(`/data/municipalities/${id}`);
    return response.data;
  }

  // Métodos para casos de arboviroses
  async getCases(params?: {
    municipality_id?: number;
    disease?: string;
    year?: number;
    start_week?: number;
    end_week?: number;
  }): Promise<ArbovirusCase[]> {
    const response: AxiosResponse<ArbovirusCase[]> = await this.api.get('/data/cases', { params });
    return response.data;
  }

  async getCasesSummary(params?: {
    disease?: string;
    year?: number;
    state?: string;
    region?: string;
  }): Promise<any> {
    const response: AxiosResponse<any> = await this.api.get('/data/cases/summary', { params });
    return response.data;
  }

  // Métodos para indicadores sociais
  async getSocialIndicators(params?: {
    municipality_id?: number;
    year?: number;
  }): Promise<SocialIndicator[]> {
    const response: AxiosResponse<SocialIndicator[]> = await this.api.get('/data/social-indicators', { params });
    return response.data;
  }

  async getCorrelationAnalysis(params?: {
    disease?: string;
    year?: number;
    indicators?: string[];
  }): Promise<any> {
    const response: AxiosResponse<any> = await this.api.get('/data/correlations', { params });
    return response.data;
  }

  // Métodos para predições
  async getPredictions(params?: {
    municipality_id?: number;
    disease?: string;
    model_name?: string;
    weeks_ahead?: number;
  }): Promise<Prediction[]> {
    const response: AxiosResponse<Prediction[]> = await this.api.get('/predictions', { params });
    return response.data;
  }

  async generatePredictions(params: {
    municipality_ids: number[];
    disease: string;
    weeks_ahead: number;
    models?: string[];
  }): Promise<any> {
    const response: AxiosResponse<any> = await this.api.post('/predictions/generate', params);
    return response.data;
  }

  async getModelPerformance(params?: {
    model_name?: string;
    disease?: string;
    municipality_id?: number;
  }): Promise<any> {
    const response: AxiosResponse<any> = await this.api.get('/predictions/performance', { params });
    return response.data;
  }

  // Métodos para alertas
  async getAlerts(params?: {
    municipality_id?: number;
    disease?: string;
    alert_level?: string;
    is_active?: boolean;
  }): Promise<Alert[]> {
    const response: AxiosResponse<Alert[]> = await this.api.get('/alerts', { params });
    return response.data;
  }

  async createAlert(alert: Partial<Alert>): Promise<Alert> {
    const response: AxiosResponse<Alert> = await this.api.post('/alerts', alert);
    return response.data;
  }

  async updateAlert(id: number, updates: Partial<Alert>): Promise<Alert> {
    const response: AxiosResponse<Alert> = await this.api.put(`/alerts/${id}`, updates);
    return response.data;
  }

  async resolveAlert(id: number): Promise<Alert> {
    const response: AxiosResponse<Alert> = await this.api.patch(`/alerts/${id}/resolve`);
    return response.data;
  }

  // Métodos para relatórios
  async generateReport(params: {
    type: 'cases' | 'predictions' | 'alerts' | 'correlations';
    format: 'pdf' | 'excel' | 'csv';
    filters: any;
  }): Promise<Blob> {
    const response: AxiosResponse<Blob> = await this.api.post('/reports/generate', params, {
      responseType: 'blob',
    });
    return response.data;
  }

  // Métodos para dados geoespaciais
  async getGeoData(params?: {
    type: 'municipalities' | 'states' | 'regions';
    level?: string;
  }): Promise<any> {
    const response: AxiosResponse<any> = await this.api.get('/data/geo', { params });
    return response.data;
  }

  // Método para health check
  async healthCheck(): Promise<any> {
    const response: AxiosResponse<any> = await this.api.get('/health');
    return response.data;
  }
}

// Instância singleton do serviço
const apiService = new ApiService();

export default apiService;

