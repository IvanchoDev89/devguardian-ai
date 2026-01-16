<?php

namespace App\Http\Middleware;

use Illuminate\Http\Middleware\ThrottleRequests;
use Illuminate\Http\Request;

class ApiRateLimit extends ThrottleRequests
{
    /**
     * Resolve the number of requests.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return int
     */
    protected function resolveRequestSignature($request)
    {
        return sha1(
            $request->method() . '|' . $request->server('SERVER_NAME') . '|' . $request->ip()
        );
    }

    /**
     * Configure the rate limiting.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return array
     */
    protected function getRateLimit($request)
    {
        return [
            'requests' => 60,
            'minutes' => 1,
        ];
    }
}
