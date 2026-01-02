<?php

declare(strict_types=1);

namespace App\Core\Domain\ValueObjects;

final readonly class FileLocation
{
    public function __construct(
        public string $filePath,
        public int $lineNumber,
        public ?int $columnNumber = null,
        public ?string $functionName = null,
        public ?string $className = null
    ) {
        $this->validate();
    }

    private function validate(): void
    {
        if (empty($this->filePath)) {
            throw new \InvalidArgumentException('File path cannot be empty');
        }

        if ($this->lineNumber < 1) {
            throw new \InvalidArgumentException('Line number must be positive');
        }

        if ($this->columnNumber !== null && $this->columnNumber < 1) {
            throw new \InvalidArgumentException('Column number must be positive');
        }
    }

    public function __toString(): string
    {
        $location = $this->filePath . ':' . $this->lineNumber;
        
        if ($this->columnNumber !== null) {
            $location .= ':' . $this->columnNumber;
        }

        if ($this->functionName !== null) {
            $location .= ' in ' . $this->functionName;
        }

        if ($this->className !== null) {
            $location .= ' (' . $this->className . ')';
        }

        return $location;
    }

    public function toArray(): array
    {
        return [
            'file_path' => $this->filePath,
            'line_number' => $this->lineNumber,
            'column_number' => $this->columnNumber,
            'function_name' => $this->functionName,
            'class_name' => $this->className,
            'formatted' => (string) $this
        ];
    }

    public static function fromArray(array $data): self
    {
        return new self(
            $data['file_path'],
            $data['line_number'],
            $data['column_number'] ?? null,
            $data['function_name'] ?? null,
            $data['class_name'] ?? null
        );
    }
}
