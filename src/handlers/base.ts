export abstract class BaseHandler {
  protected apiUrl: string;
  protected apiToken: string;

  constructor(apiUrl: string, apiToken: string) {
    this.apiUrl = apiUrl;
    this.apiToken = apiToken;
  }

  protected getDefaultDateRange(): { start_date: string; end_date: string } {
    const today = new Date();
    const thirtyDaysAgo = new Date(today);
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

    return {
      start_date: this.formatDate(thirtyDaysAgo),
      end_date: this.formatDate(today)
    };
  }

  protected formatDate(date: Date): string {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  protected buildQueryString(params: Record<string, string | undefined>): string {
    const queryParams = new URLSearchParams();
    
    for (const [key, value] of Object.entries(params)) {
      if (value !== undefined && value !== '') {
        queryParams.append(key, value);
      }
    }
    
    const queryString = queryParams.toString();
    return queryString ? `?${queryString}` : '';
  }

  protected async fetchApi(endpoint: string, queryParams: Record<string, string | undefined>): Promise<any> {
    const url = `${this.apiUrl}${endpoint}${this.buildQueryString(queryParams)}`;

    const headers: Record<string, string> = {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    };

    // Add token to headers if available
    if (this.apiToken) {
      headers['Authorization'] = `Token ${this.apiToken}`;
    }

    try {
      const response = await fetch(url, {
        method: 'GET',
        headers
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API request failed (${response.status}): ${errorText}`);
      }

      return await response.json();
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error(`Failed to fetch from API: ${String(error)}`);
    }
  }

  protected async fetchApiPost(endpoint: string, body: any): Promise<any> {
    const url = `${this.apiUrl}${endpoint}`;

    const headers: Record<string, string> = {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'Authorization': `Token ${this.apiToken}`
    };

    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status} ${response.statusText}`);
    }

    return response.json();
  }

  abstract handle(args: any): Promise<any>;
}