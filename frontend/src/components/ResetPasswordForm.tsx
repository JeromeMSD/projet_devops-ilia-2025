import type { ComponentProps } from 'react';
import { Controller, useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';
import {
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
} from '@/components/ui/card';
import {
    Field,
    FieldDescription,
    FieldError,
    FieldGroup,
    FieldLabel,
} from '@/components/ui/field';
import { Input } from '@/components/ui/input';
import { Spinner } from '@/components/ui/spinner';
import { resetPasswordSchema, type ResetPasswordValues } from '@/auth/schema/reset-password-schema.ts';
import { useResetPassword } from '@/auth/useResetPassword';

export function ResetPasswordForm({ className, ...props }: ComponentProps<'div'>) {
    const mutation = useResetPassword();
    const form = useForm<ResetPasswordValues>({
        resolver: zodResolver(resetPasswordSchema),
        defaultValues: {
            reset_token: '',
            new_password: '',
        },
    });

    function onSubmit(values: ResetPasswordValues) {
        mutation.reset();
        mutation.mutate(values, {
            onSuccess: () => {
                form.reset({
                    reset_token: '',
                    new_password: '',
                });
            },
        });
    }

    const formError = mutation.error instanceof Error ? mutation.error.message : null;
    const successMessage = mutation.data?.message ?? (mutation.isSuccess ? 'Mot de passe réinitialisé avec succès.' : null);

    return (
        <div className={cn('flex flex-col gap-6', className)} {...props}>
            <Card>
                <CardHeader>
                    <CardTitle>Réinitialiser votre mot de passe</CardTitle>
                    <CardDescription>
                        Collez le token reçu par email et choisissez un nouveau mot de passe.
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <form
                        onSubmit={form.handleSubmit(onSubmit)}
                        className="space-y-6"
                        noValidate
                    >
                        <FieldGroup>
                            <Controller
                                name="reset_token"
                                control={form.control}
                                render={({ field, fieldState }) => (
                                    <Field data-invalid={fieldState.invalid}>
                                        <FieldLabel htmlFor="reset-token">Token de réinitialisation</FieldLabel>
                                        <Input
                                            {...field}
                                            id="reset-token"
                                            type="text"
                                            placeholder="Collez votre token"
                                            aria-invalid={fieldState.invalid}
                                            disabled={mutation.isPending}
                                        />
                                        {fieldState.invalid && (
                                            <FieldError errors={[fieldState.error]} />
                                        )}
                                    </Field>
                                )}
                            />

                            <Controller
                                name="new_password"
                                control={form.control}
                                render={({ field, fieldState }) => (
                                    <Field data-invalid={fieldState.invalid}>
                                        <FieldLabel htmlFor="reset-password">Nouveau mot de passe</FieldLabel>
                                        <Input
                                            {...field}
                                            id="reset-password"
                                            type="password"
                                            placeholder="NouveauPassword123"
                                            aria-invalid={fieldState.invalid}
                                            disabled={mutation.isPending}
                                        />
                                        <FieldDescription>
                                            6 caractères min., au moins une majuscule et un chiffre.
                                        </FieldDescription>
                                        {fieldState.invalid && (
                                            <FieldError errors={[fieldState.error]} />
                                        )}
                                    </Field>
                                )}
                            />

                            {formError && (
                                <Field data-invalid>
                                    <FieldError errors={[{ message: formError }]} />
                                </Field>
                            )}

                            {successMessage && (
                                <Field>
                                    <p className="text-sm font-medium text-emerald-700">{successMessage}</p>
                                </Field>
                            )}

                            <Field>
                                <Button type="submit" disabled={mutation.isPending} className="w-full">
                                    {mutation.isPending && <Spinner />}
                                    {mutation.isPending ? 'Réinitialisation...' : 'Réinitialiser'}
                                </Button>
                            </Field>
                        </FieldGroup>
                    </form>
                </CardContent>
            </Card>
        </div>
    );
}
