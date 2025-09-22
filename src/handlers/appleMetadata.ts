import { BaseHandler } from './base.js';

export class AppleMetadataHandler extends BaseHandler {
  async handle(args: any): Promise<any> {
    const { app, data = 'title', country = 'in', language = 'en', start_date, end_date } = args;

    if (!app) {
      throw new Error('App ID is required');
    }

    // Use provided dates or default to last 30 days
    const dateRange = this.getDefaultDateRange();
    const queryParams = {
      app,
      data,
      country,
      language,
      start_date: start_date || dateRange.start_date,
      end_date: end_date || dateRange.end_date
    };

    try {
      const result = await this.fetchApi('/metadata/apple/', queryParams);
      
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(result, null, 2)
          }
        ]
      };
    } catch (error) {
      throw new Error(`Failed to fetch Apple metadata: ${error instanceof Error ? error.message : String(error)}`);
    }
  }
}