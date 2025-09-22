import { BaseHandler } from './base.js';

export class KeywordResearchHandler extends BaseHandler {
  async handle(args: any): Promise<any> {
    const { keywords, country = 'in', language = 'en', platform = 'android' } = args;

    if (!keywords || !Array.isArray(keywords) || keywords.length === 0) {
      throw new Error('Keywords array is required and must not be empty');
    }

    // Validate platform
    if (!['android', 'ios'].includes(platform)) {
      throw new Error('Platform must be either "android" or "ios"');
    }

    const endpoint = `/keyword-research/${platform}/`;
    const requestBody = {
      keywords,
      country,
      language,
      platform
    };

    try {
      const result = await this.fetchApiPost(endpoint, requestBody);

      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(result, null, 2)
          }
        ]
      };
    } catch (error) {
      throw new Error(`Failed to fetch keyword research data: ${error instanceof Error ? error.message : String(error)}`);
    }
  }
}