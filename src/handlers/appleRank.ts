import { BaseHandler } from './base.js';

export class AppleRankHandler extends BaseHandler {
  async handle(args: any): Promise<any> {
    const { app, country = 'in', start_date, end_date } = args;

    if (!app) {
      throw new Error('App ID is required');
    }

    // Use provided dates or default to last 30 days
    const dateRange = this.getDefaultDateRange();
    const queryParams = {
      app,
      country,
      start_date: start_date || dateRange.start_date,
      end_date: end_date || dateRange.end_date
    };

    try {
      const result = await this.fetchApi('/category/rank/apple/', queryParams);
      
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(result, null, 2)
          }
        ]
      };
    } catch (error) {
      throw new Error(`Failed to fetch Apple category ranks: ${error instanceof Error ? error.message : String(error)}`);
    }
  }
}