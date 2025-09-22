import { BaseHandler } from './base.js';

export class UserJobsHandler extends BaseHandler {
  async handle(args: any): Promise<any> {
    try {
      // User Jobs API doesn't require any parameters - uses authentication only
      const result = await this.fetchApi('/userjobs/', {});

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(result, null, 2)
          }
        ]
      };
    } catch (error) {
      throw new Error(`Failed to fetch user jobs: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

}