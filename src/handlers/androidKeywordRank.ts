import { BaseHandler } from './base.js';

export class AndroidKeywordRankHandler extends BaseHandler {
  async handle(args: any): Promise<any> {
    const { app, keywords, country = 'in', language = 'en', start_date, end_date, date } = args;

    if (!app) {
      throw new Error('App package name is required');
    }

    if (!keywords) {
      throw new Error('Keywords are required');
    }

    // Use provided dates or default to last 30 days if neither date nor start_date/end_date provided
    const dateRange = this.getDefaultDateRange();
    const queryParams: Record<string, string | undefined> = {
      app,
      keywords,
      country,
      language
    };

    // Handle date parameters - either use 'date' for single date or start_date/end_date for range
    if (date) {
      queryParams.date = date;
    } else {
      queryParams.start_date = start_date || dateRange.start_date;
      queryParams.end_date = end_date || dateRange.end_date;
    }

    try {
      const result = await this.fetchApi('/ranks/android/', queryParams);

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(result, null, 2)
          }
        ]
      };
    } catch (error) {
      throw new Error(`Failed to fetch Android keyword ranks: ${error instanceof Error ? error.message : String(error)}`);
    }
  }
}